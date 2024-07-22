# Feature-requests-1
get_html(link):

Fetches HTML content from the provided URL (link).
get_soup(html):

Creates a BeautifulSoup object from the HTML content.
get_details(soup):

Extracts doctor details (name, qualifications, specialities, addresses, phone numbers) from the parsed HTML.
write_into_csv(all_data):

Writes the extracted data into a CSV file (Doctors_informations.csv).
main():

Controls the flow of execution:
Iterates through multiple pages of the website.
Scrapes data using get_html, get_soup, and get_details.
Writes data to CSV using write_into_csv.

Output:
The script generates a CSV file (Doctors_informations.csv) containing columns for:
Doctor's name (Dr Name)
Qualification (Qualification)
Specialties (Specialities)
Practice locations (Practice Locations)
Phone number (Phone)
