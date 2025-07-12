from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# PostgreSQL connection URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://job_portal_db:job_portal_db@jobportaldb.cnq2yy6e0e7a.us-east-2.rds.amazonaws.com:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define JobProfile model
class JobProfile(db.Model):
    __tablename__ = 'job_profiles_review_v4'

    id = db.Column(db.Integer, primary_key=True)
    job_profile = db.Column(db.Text)
    job_code = db.Column(db.BigInteger)
    job_category = db.Column(db.Text)
    job_profile_name = db.Column(db.Text)
    vertical = db.Column(db.Text)
    division = db.Column(db.Text)
    subdivision = db.Column(db.Text)
    primary_reviewer = db.Column(db.Text)
    hr_reviewer = db.Column(db.Text)
    hiring_manager = db.Column(db.Text)
    recruiter_reviewer = db.Column(db.Text)


    # Finalized fields
    position_purpose = db.Column(db.Text)
    key_responsibilities = db.Column(db.Text)
    direct_manager_direct_reports = db.Column(db.Text)
    travel_requirements = db.Column(db.Text)
    physical_requirements = db.Column(db.Text)
    working_conditions = db.Column(db.Text)
    minimum_qualifications = db.Column(db.Text)
    preferred_qualifications = db.Column(db.Text)
    minimum_education = db.Column(db.Text)
    preferred_education = db.Column(db.Text)
    minimum_years_of_work_experience = db.Column(db.Text)
    certifications = db.Column(db.Text)
    competencies = db.Column(db.Text)
    what_you_will_do = db.Column(db.Text)
    what_we_look_for = db.Column(db.Text)
    qualities_that_stir_our_souls = db.Column(db.Text)

    # Saved (draft) fields
    saved_position_purpose = db.Column(db.Text)
    saved_key_responsibilities = db.Column(db.Text)
    saved_direct_manager_direct_reports = db.Column(db.Text)
    saved_travel_requirements = db.Column(db.Text)
    saved_physical_requirements = db.Column(db.Text)
    saved_working_conditions = db.Column(db.Text)
    saved_minimum_qualifications = db.Column(db.Text)
    saved_preferred_qualifications = db.Column(db.Text)
    saved_minimum_education = db.Column(db.Text)
    saved_preferred_education = db.Column(db.Text)
    saved_minimum_years_of_work_experience = db.Column(db.Text)
    saved_certifications = db.Column(db.Text)
    saved_competencies = db.Column(db.Text)
    saved_what_you_will_do = db.Column(db.Text)
    saved_what_we_look_for = db.Column(db.Text)
    saved_qualities_that_stir_our_souls = db.Column(db.Text)

    approved_internal = db.Column(db.Text)
    approved_external = db.Column(db.Text)


class Reviewer(db.Model):
    __tablename__ = 'reviewers_list'

    id = db.Column(db.Integer, primary_key=True)
    primary_reviewer = db.Column(db.Text)
    hr_reviewer = db.Column(db.Text)
    hiring_manager = db.Column(db.Text)



@app.route('/api/all-job-profiles', methods=['GET'])
def get_all_job_profiles():
    profiles = JobProfile.query.all()

    profiles_data = {}

    for p in profiles:
        profiles_data[p.job_profile] = {
            'primaryReviewer': p.primary_reviewer,
            'hrReviewer': p.hr_reviewer,
            'hiringManager': p.hiring_manager,
            'vertical': p.vertical,
            'division': p.division,
            'subdivision': p.subdivision,
            'description': {
                'purpose': p.saved_position_purpose or p.position_purpose,
                'responsibilities': p.saved_key_responsibilities or p.key_responsibilities,
                'manager': p.saved_direct_manager_direct_reports or p.direct_manager_direct_reports,
                'travel': p.saved_travel_requirements or p.travel_requirements,
                'physical': p.saved_physical_requirements or p.physical_requirements,
                'workconditions': p.saved_working_conditions or p.working_conditions,
                'minqualifications': p.saved_minimum_qualifications or p.minimum_qualifications,
                'preferredqualifications': p.saved_preferred_qualifications or p.preferred_qualifications,
                'mineducation': p.saved_minimum_education or p.minimum_education,
                'preferrededucation': p.saved_preferred_education or p.preferred_education,
                'minexperience': p.saved_minimum_years_of_work_experience or p.minimum_years_of_work_experience,
                'certifications': p.saved_certifications or p.certifications,
                'competencies': p.saved_competencies or p.competencies
            }
        }

    return jsonify(profiles_data)

@app.route('/api/internal/all-job-profiles', methods=['GET'])
def get_all_job_profiles_internal():
    profiles = JobProfile.query.all()

    profiles_data = {}

    for p in profiles:
        profiles_data[p.job_profile] = {
            'primaryReviewer': p.primary_reviewer,
            'hrReviewer': p.hr_reviewer,
            'hiringManager': p.hiring_manager,
            'vertical': p.vertical,
            'division': p.division,
            'subdivision': p.subdivision,
            'description': {
                'purpose': p.saved_position_purpose or p.position_purpose,
                'responsibilities': p.saved_key_responsibilities or p.key_responsibilities,
                'manager': p.saved_direct_manager_direct_reports or p.direct_manager_direct_reports,
                'travel': p.saved_travel_requirements or p.travel_requirements,
                'physical': p.saved_physical_requirements or p.physical_requirements,
                'workconditions': p.saved_working_conditions or p.working_conditions,
                'minqualifications': p.saved_minimum_qualifications or p.minimum_qualifications,
                'preferredqualifications': p.saved_preferred_qualifications or p.preferred_qualifications,
                'mineducation': p.saved_minimum_education or p.minimum_education,
                'preferrededucation': p.saved_preferred_education or p.preferred_education,
                'minexperience': p.saved_minimum_years_of_work_experience or p.minimum_years_of_work_experience,
                'certifications': p.saved_certifications or p.certifications,
                'competencies': p.saved_competencies or p.competencies,
            },
            'approved_internal': p.approved_internal,
        }

    return jsonify(profiles_data)

@app.route('/api/reviewers-list', methods=['GET'])
def get_reviewers_list():
    profiles = JobProfile.query.all()

    profile_primary_reviewers = [p.primary_reviewer for p in profiles if p.primary_reviewer]
    profile_hr_reviewers = [p.hr_reviewer for p in profiles if p.hr_reviewer]
    profile_hiring_managers = [p.hiring_manager for p in profiles if p.hiring_manager]

    reviewers = Reviewer.query.all()

    new_primary_reviewers = [r.primary_reviewer for r in reviewers if r.primary_reviewer]
    new_hr_reviewers = [r.hr_reviewer for r in reviewers if r.hr_reviewer]
    new_hiring_managers = [r.hiring_manager for r in reviewers if r.hiring_manager]

    primary_reviewers = list(set(profile_primary_reviewers + new_primary_reviewers))
    hr_reviewers = list(set(profile_hr_reviewers + new_hr_reviewers))
    hiring_managers = list(set(profile_hiring_managers + new_hiring_managers))

    return jsonify({
        'primaryReviewers': primary_reviewers,
        'hrReviewers': hr_reviewers,
        'managers': hiring_managers
    })

@app.route('/api/admin-reviewers/add', methods=['POST'])
def add_admin_reviewer():
    data = request.get_json()
    name = data.get('name')
    reviewer_type = data.get('type')

    if not name or not reviewer_type:
        return jsonify({'error': 'Name and type are required'}), 400

    if reviewer_type not in ['primary', 'hr', 'manager']:
        return jsonify({'error': 'Invalid reviewer type'}), 400

    new_reviewer = Reviewer(
        primary_reviewer=name if reviewer_type == 'primary' else None,
        hr_reviewer=name if reviewer_type == 'hr' else None,
        hiring_manager=name if reviewer_type == 'manager' else None
    )

    db.session.add(new_reviewer)
    db.session.commit()

    return jsonify({'message': f'{reviewer_type.capitalize()} reviewer added successfully'}), 200

@app.route('/api/admin-review/update', methods=['POST'])
def update_admin_review():
    try:
        data = request.get_json()

        profile_name = data.get('profile')
        updated_data = data.get('updatedData')

        if not profile_name or not updated_data:
            return jsonify({'error': 'Profile name and updated data are required'}), 400

        job = JobProfile.query.filter_by(job_profile=profile_name).first()


        if not job:
            return jsonify({'error': 'Job profile not found'}), 404

        job.primary_reviewer = updated_data.get('primaryReviewer')
        job.hr_reviewer = updated_data.get('hrReviewer')
        job.hiring_manager = updated_data.get('hiringManager')
        job.vertical = updated_data.get('vertical')
        job.division = updated_data.get('division')
        job.subdivision = updated_data.get('subdivision')
        
        job.saved_position_purpose = updated_data.get('purpose')
        job.saved_key_responsibilities = updated_data.get('responsibilities')
        job.saved_direct_manager_direct_reports = updated_data.get('manager')
        job.saved_travel_requirements = updated_data.get('travel')
        job.saved_physical_requirements = updated_data.get('physical')
        job.saved_working_conditions = updated_data.get('workconditions')
        job.saved_minimum_qualifications = updated_data.get('minqualifications')
        job.saved_preferred_qualifications = updated_data.get('preferredqualifications')
        job.saved_minimum_education = updated_data.get('mineducation')
        job.saved_preferred_education = updated_data.get('preferrededucation')
        job.saved_minimum_years_of_work_experience = updated_data.get('minexperience')
        job.saved_certifications = updated_data.get('certifications')
        job.saved_competencies = updated_data.get('competencies')

        db.session.commit()

        return jsonify({'message': 'Profile updated successfully'}), 200

    except Exception as e:
        print(f"Error updating profile: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/api/internal-review/save', methods=['POST'])
def save_internal_review():
    try:
        data = request.get_json()

        profile_name = data.get('profile')
        updated_data = data.get('updatedData')

        if not profile_name or not updated_data:
            return jsonify({'error': 'Profile name and updated data are required'}), 400

        job = JobProfile.query.filter_by(job_profile=profile_name).first()

        if not job:
            return jsonify({'error': 'Job profile not found'}), 404

        job.saved_position_purpose = updated_data.get('purpose')
        job.saved_key_responsibilities = updated_data.get('responsibilities')
        job.saved_direct_manager_direct_reports = updated_data.get('manager')
        job.saved_travel_requirements = updated_data.get('travel')
        job.saved_physical_requirements = updated_data.get('physical')
        job.saved_working_conditions = updated_data.get('workconditions')
        job.saved_minimum_qualifications = updated_data.get('minqualifications')
        job.saved_preferred_qualifications = updated_data.get('preferredqualifications')
        job.saved_minimum_education = updated_data.get('mineducation')
        job.saved_preferred_education = updated_data.get('preferrededucation')
        job.saved_minimum_years_of_work_experience = updated_data.get('minexperience')
        job.saved_certifications = updated_data.get('certifications')
        job.saved_competencies = updated_data.get('competencies')

        db.session.commit()

        return jsonify({'message': 'Profile updated successfully'}), 200

    except Exception as e:
        print(f"Error updating profile: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    

@app.route('/api/internal-review/approve', methods=['POST'])
def approve_internal_review():
    try:
        data = request.get_json()

        profile_name = data.get('profile')
        updated_data = data.get('updatedData')

        if not profile_name or not updated_data:
            return jsonify({'error': 'Profile name and updated data are required'}), 400

        job = JobProfile.query.filter_by(job_profile=profile_name).first()

        if not job:
            return jsonify({'error': 'Job profile not found'}), 404

        print(updated_data)
        
        job.saved_position_purpose = updated_data.get('purpose')
        job.saved_key_responsibilities = updated_data.get('responsibilities')
        job.saved_direct_manager_direct_reports = updated_data.get('manager')
        job.saved_travel_requirements = updated_data.get('travel')
        job.saved_physical_requirements = updated_data.get('physical')
        job.saved_working_conditions = updated_data.get('workconditions')
        job.saved_minimum_qualifications = updated_data.get('minqualifications')
        job.saved_preferred_qualifications = updated_data.get('preferredqualifications')
        job.saved_minimum_education = updated_data.get('mineducation')
        job.saved_preferred_education = updated_data.get('preferrededucation')
        job.saved_minimum_years_of_work_experience = updated_data.get('minexperience')
        job.saved_certifications = updated_data.get('certifications')
        job.saved_competencies = updated_data.get('competencies')
        job.approved_internal = updated_data.get('approved_internal')

        db.session.commit()

        return jsonify({'message': 'Profile updated successfully'}), 200

    except Exception as e:
        print(f"Error updating profile: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    

@app.route('/api/external/all-job-profiles', methods=['GET'])
def get_all_job_profiles_external():
    profiles = JobProfile.query.all()

    profiles_data = {}

    for p in profiles:
        profiles_data[p.job_profile] = {
            'primaryReviewer': p.primary_reviewer,
            'hrReviewer': p.hr_reviewer,
            'hiringManager': p.hiring_manager,
            'vertical': p.vertical,
            'division': p.division,
            'subdivision': p.subdivision,
            'recruiterReviewer': p.recruiter_reviewer,
            'description': {
                'purpose': p.saved_position_purpose or p.position_purpose,
                'responsibilities': p.saved_key_responsibilities or p.key_responsibilities,
                'manager': p.saved_direct_manager_direct_reports or p.direct_manager_direct_reports,
                'travel': p.saved_travel_requirements or p.travel_requirements,
                'physical': p.saved_physical_requirements or p.physical_requirements,
                'workconditions': p.saved_working_conditions or p.working_conditions,
                'minqualifications': p.saved_minimum_qualifications or p.minimum_qualifications,
                'preferredqualifications': p.saved_preferred_qualifications or p.preferred_qualifications,
                'mineducation': p.saved_minimum_education or p.minimum_education,
                'preferrededucation': p.saved_preferred_education or p.preferred_education,
                'minexperience': p.saved_minimum_years_of_work_experience or p.minimum_years_of_work_experience,
                'certifications': p.saved_certifications or p.certifications,
                'competencies': p.saved_competencies or p.competencies,
                'whatYoullDo' : p.saved_what_you_will_do or p.what_you_will_do,
                'whatWeLookFor': p.saved_what_we_look_for or p.what_we_look_for,
                'qualitiesThatStir': p.saved_qualities_that_stir_our_souls or p.qualities_that_stir_our_souls
            },
            'approved_internal': p.approved_internal,
            'approved_external': p.approved_external
        }

    return jsonify(profiles_data)


@app.route('/api/external-review/save', methods=['POST'])
def save_external_review():
    try:
        data = request.get_json()

        profile_name = data.get('profile')
        updated_data = data.get('updatedRecruiterDescription')

        print(profile_name)
        print(updated_data)

        if not profile_name or not updated_data:
            return jsonify({'error': 'Profile name and updated data are required'}), 400

        job = JobProfile.query.filter_by(job_profile=profile_name).first()

        if not job:
            return jsonify({'error': 'Job profile not found'}), 404

        job.saved_what_you_will_do = updated_data.get('whatYoullDo')
        job.saved_what_we_look_for = updated_data.get('whatWeLookFor')
        job.saved_qualities_that_stir_our_souls = updated_data.get('qualitiesThatStir')

        db.session.commit()

        return jsonify({'message': 'Profile updated successfully'}), 200

    except Exception as e:
        print(f"Error updating profile: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    

@app.route('/api/external-review/approve', methods=['POST'])
def approve_external_review():
    try:
        data = request.get_json()

        profile_name = data.get('profile')
        updated_data = data.get('updatedRecruiterDescription')

        if not profile_name or not updated_data:
            return jsonify({'error': 'Profile name and updated data are required'}), 400

        job = JobProfile.query.filter_by(job_profile=profile_name).first()

        if not job:
            return jsonify({'error': 'Job profile not found'}), 404

        
        job.saved_what_you_will_do = updated_data.get('whatYoullDo')
        job.saved_what_we_look_for = updated_data.get('whatWeLookFor')
        job.saved_qualities_that_stir_our_souls = updated_data.get('qualitiesThatStir')
        job.approved_external = updated_data.get('approved_external')

        db.session.commit()

        return jsonify({'message': 'Profile updated successfully'}), 200

    except Exception as e:
        print(f"Error updating profile: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/recuriter_reviewers-list', methods=['GET'])
def get_recruiter_reviewers_list():
    profiles = JobProfile.query.all()

    profile_recruiter_reviewers = [p.primary_reviewer for p in profiles if p.primary_reviewer]

    reviewers = Reviewer.query.all()


    new_primary_reviewers = [r.primary_reviewer for r in reviewers if r.primary_reviewer]

    primary_reviewers = list(set(profile_recruiter_reviewers + new_primary_reviewers))


    return jsonify({
        'recruiterReviewers': list(set(primary_reviewers)),
    })


@app.route('/api/job-profile/<job_profile>', methods=['GET'])
def get_job_profile_by_name(job_profile):
    job = JobProfile.query.filter_by(job_profile=job_profile).first()

    if not job:
        return jsonify({'error': 'Job Profile not found'}), 404

    response_data = {
        'id': job.id,
        'job_profile': job.job_profile,
        'job_code': job.job_code,
        'job_category': job.job_category,
        'job_profile_name': job.job_profile_name,
        'vertical': job.vertical,
        'division': job.division,
        'subdivision': job.subdivision,
        'primary_reviewer': job.primary_reviewer,
        'hr_reviewer': job.hr_reviewer,
        'hiring_manager': job.hiring_manager
    }

    field_names = [
        'position_purpose',
        'key_responsibilities',
        'direct_manager_direct_reports',
        'travel_requirements',
        'physical_requirements',
        'working_conditions',
        'minimum_qualifications',
        'preferred_qualifications',
        'minimum_education',
        'preferred_education',
        'minimum_years_of_work_experience',
        'certifications',
        'competencies',
        'what_you_will_do',
        'what_we_look_for',
        'qualities_that_stir_our_souls'
    ]

    for field in field_names:
        saved_field = f"saved_{field}"  

        saved_value = getattr(job, saved_field)
        final_value = getattr(job, field)

        if saved_value and saved_value.strip():
            response_data[field] = saved_value
        else:
            response_data[field] = final_value

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
