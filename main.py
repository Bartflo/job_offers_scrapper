import aiohttp
import asyncio
from bs4 import BeautifulSoup

async def fetch_page(session, url):
    async with session.get(url) as response:
        html_content = await response.text()
        return BeautifulSoup(html_content, 'html.parser')

async def main():
    base_url = "https://nofluffjobs.com"
    urls = [
        "https://nofluffjobs.com/pl/lodz?criteria=seniority%3Dtrainee,junior&sort=newest"
    ]
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(fetch_page(session, url))
            
        htmls = await asyncio.gather(*tasks)

    for soup in htmls:
        container = soup.find('div', class_='list-container')
        if container:
            job_listings = container.find_all('a', class_='posting-list-item')
            
            for job in job_listings:

                title = job.find('h3', class_='posting-title__position').text.strip()
                company = job.find('h4', class_='company-name').text.strip()
                location = job.find('span', class_='tw-text-ellipsis').text.strip()
                link = base_url + job.get('href')
                salary = job.find('span', {'data-cy': 'salary ranges on the job offer listing'}).text.strip()
                categories = []
                for tag in job.find_all('span', class_='posting-tag'):
                    if 'PLN' not in tag.text:
                        categories.append(tag.text.strip())
                
                print(f"\nJob: {title}")
                print(f"Company: {company}")
                print(f"Location: {location}")
                print(f"Salary: {salary}")
                print(f"Categories: {', '.join(categories)}")
                print(f"Link: {link}")
                print("-" * 50)

# Run the main function
asyncio.run(main())