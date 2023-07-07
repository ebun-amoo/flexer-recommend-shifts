import requests

#gets json object from from url
def call_api(url):
    try:
        response = requests.get(url)
        # Raise an exception for non-2xx status codes
        response.raise_for_status()  
        data = response.json() 
        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    

def record_application_data():
    api_url = "https://flexie-app.directus.app/items/APPLICATIONS?fields=id,%20accepted,%20shift_status,%20shift.*,%20flexer.*,%20shift_revenue,%20check_in_time,%20check_out_time,%20shift.job.*"  
    api_data = call_api(api_url)['data']
    
    #uses a dictionary to record flexers job history
    flexer_job_records = {}
    for i in range(0, len(api_data)):
        flexer_id = api_data[i]['flexer']['id']
        job_role = api_data[i]['shift']['job']['role']
        
        #records the different jobs and the number of times the flexer has taken them
        if flexer_id not in flexer_job_records:
            flexer_job_records[flexer_id] = {job_role: 1}
        else:
            if job_role in flexer_job_records[flexer_id]:
                flexer_job_records[flexer_id][job_role] += 1
            else:
                flexer_job_records[flexer_id][job_role] = 1
    return flexer_job_records

#checks if the given ID is in the FLEXERS json object
def check_flexers_records(flexer_id):
    flexer_url = 'https://flexie-app.directus.app/items/FLEXERS'
    flexer_data = call_api(flexer_url)['data']
    for i in range(0, len(flexer_data)):
        if flexer_id == flexer_data[i]['id']:
            return True
        
    return False
        
#checks if the given ID is in the APPLICATONS json object
def check_applications_records(flexer_id):
    applications_url = 'https://flexie-app.directus.app/items/APPLICATIONS'
    applications_data = call_api(applications_url)['data']
    for i in range(0, len(applications_data)):
        if flexer_id == applications_data[i]['flexer']:
            return True
        
    return False
        
#prints (recommends) jobs flexer has taken before
def show_recommendations_to_user(flexer_id):
    flexer_job_records = record_application_data()
    flexer_jobs = flexer_job_records[flexer_id]
    print('Job Recommendations')
    for job in flexer_jobs:
        print(f'{job} --- Taken {flexer_jobs[job]} time(s)')
        
#requests flexer's id and prints results
def recommend_jobs_to_flexer():
    while True:
        print('\nPress Enter key to break loop')
        flexer_id = input('Enter flexer id: ')
        if not flexer_id:
            break
        
        valid = check_flexers_records(flexer_id)
        applied = check_applications_records(flexer_id)
        if valid is False:
            print(f'This ID is not recognized')
        elif applied is False:
            print(f'This Flexer has not applied for any jobs yet')
        elif valid is True and applied is True:
            show_recommendations_to_user(flexer_id)
        

recommend_jobs_to_flexer()