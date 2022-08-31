from sqlalchemy import create_engine, text


DB_URI = "postgresql://cmmiterative:cmmiterativepasswd@159.89.235.182:5432/iterativeactivitiescmm"













# Rutina 1
def get_activities(id_course):
    out = {}
    try:
        query = "SELECT id, activity_name, last_stage FROM Activity WHERE id_course = '{}';".format(id_course)
        engine = create_engine(DB_URI)
        with engine.begin() as conn:
            result = conn.execute(text(query))
            out["result"] = []
            for row in result:
                out["result"].append((row[0], row[1], row[2]))
    except:
        out["error"] = "db-error"
    return out


# Rutina 2
def get_submission(id_activity, id_student, stage):
    out = {}
    try:
        query = "SELECT submission, submission_time FROM Submission WHERE id_activity = {} AND id_student = '{}' AND stage = {};".format(id_activity, id_student, stage)
        engine = create_engine(DB_URI)
        with engine.begin() as conn:
            result = conn.execute(text(query))
            first = result.first()
            if first is not None:
                out["result"] = (first[0], first[1].strftime("%m/%d/%Y %H:%M:%S"))
            else:
                out["error"] = "submission-not-found"
    except:
        out["error"] = "db-error"
    return out


# Rutina 3
def create_or_edit_activity(id_course, activity_name):
    out = {}
    try:
        engine = create_engine(DB_URI)
        with engine.begin() as conn:
            query1 = "SELECT * FROM Activity WHERE id_course = '{}' AND activity_name = '{}';".format(id_course, activity_name)
            result1 = conn.execute(text(query1))
            first = result1.first()
            if first is not None:
                stage = first[3] + 1
                query2 = "UPDATE Activity SET last_stage = {} WHERE id_course = '{}' AND activity_name = '{}';".format(stage, id_course, activity_name)
            else:
                stage = 1
                query2 = "INSERT INTO Activity (id_course, activity_name, last_stage) VALUES ('{}', '{}', 1);".format(id_course, activity_name)
            conn.execute(text(query2))
            out["stage"] = stage
    except Exception as e:
        print(e)
        out["error"] = "db-error"
    return out


# Rutina 4
def add_submission(id_activity, id_student, stage, submission):
    out = {}
    try:
        query = "INSERT INTO Submission (id_activity, id_student, stage, submission, submission_time) VALUES ({}, '{}', {}, '{}', now());".format(id_activity, id_student, stage, submission)
        engine = create_engine(DB_URI)
        with engine.begin() as conn:
            conn.execute(text(query))
        out["result"] = "success"
    except:
        out["error"] = "db-error"
    return out

# Rutina 5
def get_available_submissions(id_activity, stage):
    out = {}
    try:
        query = "SELECT id_student, submission, submission_time FROM Submission WHERE id_activity = {} AND stage = {};".format(id_activity, stage)
        engine = create_engine(DB_URI)
        with engine.begin() as conn:
            result = conn.execute(text(query))
        for row in result:
            out[str(row[0])] = {
                "submission": row[1],
                "submission_time": row[2]
            }
    except:
        out["error"] = "db-error"
    return out

# Rutina 6
def add_feedbacks(id_activity, id_student, stage, feedbacks):
    out = {}
    try:
        engine = create_engine(DB_URI)
        with engine.begin() as conn:
            for element in feedbacks:
                query = "INSERT INTO Feedback (id_activity, id_student, id_instructor, stage, feedback, feedback_time) VALUES ({}, '{}', '{}', {}, '{}', now());".format(id_activity, id_student, element[0], stage, element[1])
                conn.execute(text(query))
        out["result"] = "success"
    except:
        out["error"] = "db-error"
    return out


# Rutina 7
def get_summary(id_activity, id_student):
    out = {}
    try:
        query = "SELECT stage, submission, submission_time FROM Submission WHERE id_activity = {} AND id_student = '{}';".format(id_activity, id_student)
        engine = create_engine(DB_URI)
        with engine.begin() as conn:
            result = conn.execute(text(query))
        out["result"] = []
        for row in result:
            out["result"].append((row[0], row[1], row[2].strftime("%m/%d/%Y %H:%M:%S")))
    except:
        out["error"] = "db-error"
    return out


# Rutina 8
def get_feedbacks(id_activity, id_student, stage):
    out = {}
    try:
        query = "SELECT id_instructor, feedback, feedback_time FROM Feedback WHERE id_activity = {} AND id_student = '{}' AND stage = {};".format(id_activity, id_student, stage)
        engine = create_engine(DB_URI)
        with engine.begin() as conn:
            result = conn.execute(text(query))
        for row in result:
            out[row[0]] = {
                "feedback": row[1],
                "feedback_time": row[2]
            }
    except:
        out["error"] = "db-error"
    return out

# Rutina 9
def get_id_activity(id_course, activity_name):
    out = {}
    try:
        query = "SELECT id FROM Activity WHERE id_course = '{}' AND activity_name = '{}';".format(id_course, activity_name)
        engine = create_engine(DB_URI)
        with engine.begin() as conn:
            result = conn.execute(text(query))
        first = result.first()
        if first is not None:
            out["result"] = first[0]
        else:
            out["error"] = "activity-not-found"
    except:
        out["error"] = "db-error"
    return out