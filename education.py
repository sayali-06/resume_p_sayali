import re
import spacy
from nltk.corpus import stopwords

# load pre-trained model
nlp = spacy.load('en_core_web_sm')

# Grad all general stop words
STOPWORDS = set(stopwords.words('english'))
resume_text = ''' CONTACT DETAILS 1737 Marshville Road,  Alabama (123)-456-7899 info@qwikresume.com  www.qwikresume.com  SKILLS Cloudera Hadoop, HDFS,  HIVE, CASSANDRA,  MongoDB, KAFKA, Spark, Scala, R-Programming,  Python-Data Structures,  Python-NLP, Python- Sentiment Analysis,  Tableau, Tibco, And  Spotfire.  LANGUAGES English (Native) French (Professional) Spanish (Professional)  INTERESTS Climbing Snowboarding Cooking Reading  REFERENCES Reference – 1 (Company  Name) Reference – 2 (Company  Name)  Robert Smith  Data Analyst I  PERSONAL STATEMENT  2+ years of 
experience as a Data Analyst is looking to secure a position  with a progressive company that appreciates a strong work ethic and who  will utilize my skills and attention to detail to work toward a common goal  as a team to benefit the company and its employees.  WORK EXPERIENCE Data Analyst I Inspironics Corporation -   August 2017 – Present   Responsibilities:  This project is for a swimming pool installation and maintenance. As   part of this project developing analytical reports to get insight into their  customer base spread over us, to study the demographics of the clients  device installations, find opportunities for business development.  Developing an analytical product for warranty management using   power BI, SQL Server, Azure and power BI gateway.   Generating an analytical report for warranty costs incurred on various   parameters such as product types, product names, part numbers,  warranty timelines, supplier locations, regions, states and customer  locations.   Developing Python modules in NLTK (natural language toolkit) -part of   speech (pos) for capturing failure 
types from problem description to  categorize the problem types and device types to perform root-cause  analysis.   Performing analysis and designing and developing the programs for   decoding warranty serial numbers to find the manufacturing date. This  data would help the 
clients to find out after how many days, months  and years the product has failed at the customer location.   Performing requirement analysis to study the installation of devices  such as heater, pumps, filters, whatever ph level requirements, log  messages.   Installing SQL Server DB and power BI, moved customer data given in   CSV format into SQL Server DB.  Sr. Data Analyst Barclays -   November 2016 – July 2017   Responsibilities:  Worked in the CCAR group for the projection of 9q for capital funding.   The client requires to find out the 
projection for capital funds for 9  quarters in series in order to identify and mitigate risks involved in  capital funds being maintained. Worked in report generation process in  hive and Oracle database based on various account codes.   Developed AVRO files for defining the data structure. Created tables in  hive using Avro files and partition strategy. Developed ETL-Java code to  load data into hive tables.   Developed codes in spark-scala to load data from CSV files into hive   © This Free Resume Template is the copyright of Qwikresume.com. Usage Guidelines  ♀tables.   Developed data compare tool in Scala and hash map to compare the  records between various sources such as CSV, Excel and hive tables.  Developed tools in Scala to query Oracle data base and retrieve the  results into csv/excel to analyze the impact of moniker SQL as part of  upcoming changes in data files.   Developed tools in Scala to verify the reports generated from fixed form reports against target expected reports for each cell of the matrix as it  is complex to verify the output manually.   Developed tools 
in the programming to generate sqls in run time as   part of functional reporting requirements to query data from hive/oracle tables.  Education  Masters in Analytics - 2016 to 2017(Harrisburg University )Master in  Computer Applications - (Annamalai University  - Chidambaram, Tamil  Nadu )Bachelor Of Science in Physics - (Baharathidasan University )  © This Free Resume Template is the copyright of Qwikresume.com. '''
# Education Degrees
EDUCATION = [
            'BE','B.E.','BCOM', 'B.E', 'BS', 'B.S', 
            'ME', 'M.E', 'M.E.', 'M.S', 'MS', 'MASTERS',
            'BTECH', 'B.TECH', 'M.TECH', 'MTECH', 
            'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII'
        ]

def extract_education(resume_text):
    nlp_text = nlp(resume_text)

    # Sentence Tokenizer
    nlp_text = [sent.text.strip() for sent in nlp_text.sents]

    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            # Replace all special symbols
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            if tex.upper() in EDUCATION and tex not in STOPWORDS:
                edu[tex] = text + nlp_text[index ]

    # Extract year
    education = []
    for key in edu.keys():
        year = re.search(re.compile(r'(((20|19)(\d{2})))'), edu[key])
        if year:
            education.append((key, ''.join(year[0])))
        else:
            education.append(key)
    return education

