from flask import Flask, request, jsonify, render_template, send_file, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from io import StringIO, BytesIO
import csv, os, re, uuid
from datetime import datetime, date

app=Flask(__name__)
app.config["SECRET_KEY"]=os.environ.get("SECRET_KEY","change-this-secret-key-before-deploying")
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///jobtracker.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["UPLOAD_FOLDER"]=os.path.join(app.root_path,"uploads")
os.makedirs(app.config["UPLOAD_FOLDER"],exist_ok=True)
db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),nullable=False)
    email=db.Column(db.String(160),unique=True,nullable=False)
    password=db.Column(db.String(255),nullable=False)

class Job(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    company=db.Column(db.String(100),nullable=False)
    role=db.Column(db.String(120),nullable=False)
    location=db.Column(db.String(120),default="")
    date_applied=db.Column(db.String(10),nullable=False)
    status=db.Column(db.String(20),default="Applied")
    link=db.Column(db.String(500),default="")
    notes=db.Column(db.Text,default="")
    recruiter=db.Column(db.String(120),default="")
    interview_date=db.Column(db.String(30),default="")
    priority=db.Column(db.String(20),default="Medium")
    resume_version=db.Column(db.String(120),default="")
    history=db.Column(db.Text,default="[]")
    resume_filename=db.Column(db.String(255),default="")
    resume_original=db.Column(db.String(255),default="")

VALID={"Applied","Interview","Offer","Rejected"}
def auth_required(fn):
    @wraps(fn)
    def wrapper(*args,**kwargs):
        if not session.get("user_id"): return jsonify({"error":"Please log in first."}),401
        return fn(*args,**kwargs)
    return wrapper

def job_json(j):
    return {k:getattr(j,k) for k in ["id","company","role","location","date_applied","status","link","notes","recruiter","interview_date","priority","resume_version","history","resume_filename","resume_original"]}

@app.route("/")
def index(): return render_template("index.html")

@app.post("/api/register")
def register():
    d=request.get_json() or {}
    name=str(d.get("name","")).strip(); email=str(d.get("email","")).strip().lower(); pw=str(d.get("password",""))
    if not name or not email or len(pw)<8: return jsonify(error="Enter name, email and a password of at least 8 characters."),400
    if User.query.filter_by(email=email).first(): return jsonify(error="An account with that email already exists."),409
    u=User(name=name,email=email,password=generate_password_hash(pw)); db.session.add(u); db.session.commit()
    session["user_id"]=u.id; session["name"]=u.name
    return jsonify(name=u.name,email=u.email)

@app.post("/api/login")
def login():
    d=request.get_json() or {}; email=str(d.get("email","")).strip().lower(); pw=str(d.get("password",""))
    u=User.query.filter_by(email=email).first()
    if not u or not check_password_hash(u.password,pw): return jsonify(error="Email or password is incorrect."),401
    session["user_id"]=u.id; session["name"]=u.name
    return jsonify(name=u.name,email=u.email)

@app.post("/api/logout")
def logout(): session.clear(); return jsonify(ok=True)

@app.get("/api/me")
def me():
    if not session.get("user_id"): return jsonify(user=None)
    return jsonify(user={"name":session.get("name")})

@app.get("/api/jobs")
@auth_required
def get_jobs():
    jobs=Job.query.filter_by(user_id=session["user_id"]).all()
    return jsonify([job_json(j) for j in jobs])

@app.post("/api/jobs")
@auth_required
def create_job():
    d=request.get_json() or {}
    if not str(d.get("company","")).strip() or not str(d.get("role","")).strip() or not d.get("date_applied"):
        return jsonify(error="Company, role and application date are required."),400
    status=d.get("status","Applied")
    if status not in VALID: return jsonify(error="Invalid status."),400
    j=Job(user_id=session["user_id"],company=d["company"].strip(),role=d["role"].strip(),
      location=d.get("location",""),date_applied=d["date_applied"],status=status,
      link=d.get("link",""),notes=d.get("notes",""),recruiter=d.get("recruiter",""),
      interview_date=d.get("interview_date",""),priority=d.get("priority","Medium"),
      resume_version=d.get("resume_version",""),history='[]')
    db.session.add(j); db.session.commit()
    return jsonify(job_json(j)),201

@app.put("/api/jobs/<int:jid>")
@auth_required
def update_job(jid):
    j=Job.query.filter_by(id=jid,user_id=session["user_id"]).first_or_404()
    d=request.get_json() or {}
    for key in ["company","role","location","date_applied","status","link","notes","recruiter","interview_date","priority","resume_version"]:
        if key in d: setattr(j,key,d[key])
    if j.status not in VALID: return jsonify(error="Invalid status."),400
    hist=__import__("json").loads(j.history or "[]")
    hist.append({"status":j.status,"at":datetime.now().isoformat(timespec="minutes")})
    j.history=__import__("json").dumps(hist[-30:])
    db.session.commit()
    return jsonify(job_json(j))

@app.delete("/api/jobs/<int:jid>")
@auth_required
def delete_job(jid):
    j=Job.query.filter_by(id=jid,user_id=session["user_id"]).first_or_404()
    db.session.delete(j); db.session.commit(); return jsonify(ok=True)

@app.get("/api/export.csv")
@auth_required
def export_csv():
    out=StringIO(); w=csv.writer(out)
    cols=["company","role","location","date_applied","status","link","notes","recruiter","interview_date","priority","resume_version"]
    w.writerow(cols)
    for j in Job.query.filter_by(user_id=session["user_id"]).all(): w.writerow([getattr(j,c) for c in cols])
    mem=BytesIO(out.getvalue().encode("utf-8-sig")); mem.seek(0)
    return send_file(mem,mimetype="text/csv",as_attachment=True,download_name="jobtracker-applications.csv")


@app.post("/api/jobs/<int:jid>/resume")
@auth_required
def upload_resume(jid):
    from werkzeug.utils import secure_filename
    j=Job.query.filter_by(id=jid,user_id=session["user_id"]).first_or_404()
    f=request.files.get("resume")
    if not f or not f.filename: return jsonify(error="Choose a PDF resume first."),400
    original=secure_filename(f.filename)
    if not original.lower().endswith(".pdf"): return jsonify(error="Only PDF resumes are allowed."),400
    head=f.stream.read(5); f.stream.seek(0)
    if head != b"%PDF-": return jsonify(error="Selected file is not a valid PDF."),400
    if j.resume_filename:
        old=os.path.join(app.config["UPLOAD_FOLDER"],j.resume_filename)
        if os.path.isfile(old): os.remove(old)
    stored=f"{session['user_id']}_{jid}_{uuid.uuid4().hex}.pdf"
    f.save(os.path.join(app.config["UPLOAD_FOLDER"],stored))
    j.resume_filename=stored; j.resume_original=original
    db.session.commit()
    return jsonify(ok=True,filename=original)

@app.get("/api/jobs/<int:jid>/resume")
@auth_required
def download_resume(jid):
    j=Job.query.filter_by(id=jid,user_id=session["user_id"]).first_or_404()
    if not j.resume_filename: return jsonify(error="No resume uploaded."),404
    path=os.path.join(app.config["UPLOAD_FOLDER"],j.resume_filename)
    if not os.path.isfile(path): return jsonify(error="Resume file not found."),404
    return send_file(path,mimetype="application/pdf",as_attachment=True,download_name=j.resume_original or "resume.pdf")

@app.delete("/api/jobs/<int:jid>/resume")
@auth_required
def delete_resume(jid):
    j=Job.query.filter_by(id=jid,user_id=session["user_id"]).first_or_404()
    if j.resume_filename:
        path=os.path.join(app.config["UPLOAD_FOLDER"],j.resume_filename)
        if os.path.isfile(path): os.remove(path)
    j.resume_filename=""; j.resume_original=""
    db.session.commit()
    return jsonify(ok=True)

@app.post("/api/matcher")
@auth_required
def matcher():
    d=request.get_json() or {}; resume=d.get("resume","").lower(); jd=d.get("description","").lower()
    if not resume.strip() or not jd.strip(): return jsonify(error="Paste both resume text and job description."),400
    words=lambda s:set(re.findall(r"[a-zA-Z][a-zA-Z+#.]{1,}",s))
    stop={"with","that","this","from","have","will","your","you","are","for","and","the","our","into","using","years","work","role","job"}
    required=words(jd)-stop; present=required & words(resume)
    missing=sorted(required-present)
    score=round(100*len(present)/max(1,len(required)))
    return jsonify(score=score,matched=sorted(present),missing=missing[:40],notice="This is a basic keyword overlap estimate, not an ATS score or hiring prediction.")

with app.app_context(): db.create_all()
if __name__=="__main__": app.run(debug=True)
