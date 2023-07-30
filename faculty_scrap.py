from bs4 import BeautifulSoup
import requests

def extract_faculty_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    faculty_data = []

    faculty_elements = soup.select('#main-content main div div div div div div h3 a')
    for faculty_element in faculty_elements:
        faculty_url = 'https://www.stevens.edu' + faculty_element['href']

        # Visit the faculty's profile page to extract bio and courses taught
        faculty_response = requests.get(faculty_url)
        faculty_soup = BeautifulSoup(faculty_response.text, 'html.parser')

        # Extract bio
        bio_element = faculty_soup.select_one('#experience > div > div:nth-of-type(2)')
        bio = bio_element.get_text(strip=True) if bio_element else "N/A"

        # Extract courses taught
        courses_element = faculty_soup.select_one('#courses > div > div:nth-child(2)')
        courses_taught = courses_element.get_text(strip=True) if courses_element else "N/A"

        faculty_data.append({
            'faculty_url': faculty_url,
            'bio': bio,
            'courses_taught': courses_taught
        })

    return faculty_data

def write_to_file(file_name, data, data_type):
    with open(file_name, 'w', encoding='utf-8') as file:
        for faculty in data:
            if data_type == 'profile_url':
                file.write(f"Faculty URL: {faculty['faculty_url']}\n")
            elif data_type == 'bios':
                file.write(f"Bio: {faculty.get('bio', 'N/A')}\n")
            elif data_type == 'courses_taught':
                file.write(f"Courses Taught: {faculty.get('courses_taught', 'N/A')}\n")
            file.write('\n')

if __name__ == '__main__':
    url = 'https://www.stevens.edu/school-business/faculty'
    faculty_data = extract_faculty_data(url)

    # Save faculty profile URLs in a separate file
    write_to_file('profile_urls.txt', faculty_data, data_type='profile_url')

    # Save faculty bios in a separate file
    write_to_file('bios.txt', faculty_data, data_type='bios')

    # Save courses taught in a separate file
    write_to_file('courses_taught.txt', faculty_data, data_type='courses_taught')
