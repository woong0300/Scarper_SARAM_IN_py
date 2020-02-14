import csv
import codecs

def save_to_file(jobs):
    file = open("jobs.csv", mode='w', encoding='utf-8')
    writer = csv.writer(file)
    writer.writerow(["title", "company", "location", "detail", "link"])
    for job in jobs:
        writer.writerow(list(job.values()))
    # infile = codecs.open('jobs.csv','r', encoding='utf-8')
    # outfile = codecs.open('job_reult.csv', 'w', encoding='euc_kr')

    # for line in infile:
    #     line = lien.replace(u'\xa0', ' ')
    #     outfile.write(line)
    # infile.close()
    # outfile.close()
    
    return