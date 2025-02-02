#!/bin/bash

# Ensure your environment is correctly set up

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export AUTH0_DOMAIN="morris-dev.uk.auth0.com"
export ALGORITHMS="RS256"
export AUTH0_API_AUDIENCE="casting-agency"

#Set up Flask environment
export FLASK_ENV="production"

# Local database URL
export LOCAL_DATABASE_URL="postgresql://drive:postgres@localhost:5432/casting_agency"

# Database URL for Render
export RENDER_DATABASE_URL="postgresql://casting_agency_w2mb_user:HOYwJAuTXdtFGx8NnhoRhbVJcRmOsTL8@dpg-cu41ugtds78s73cgnlh0-a.oregon-postgres.render.com/casting_agency_w2mb"

#ASSISTANT_TOKEN=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik41VTIycmRnRHUxbUJhTGVZQUlldCJ9.eyJpc3MiOiJodHRwczovL21vcnJpcy1kZXYudWsuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY3OGJkYjBmNWUwYzU2MjMyMWU5MjQ3MSIsImF1ZCI6WyJjYXN0aW5nLWFnZW5jeSIsImh0dHBzOi8vbW9ycmlzLWRldi51ay5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzM4MDczOTA1LCJleHAiOjE3MzgwODExMDUsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhenAiOiJYbHQyVEpDd05vVGo2VWJpb0VXMVc0TlpuUlJIVnhIMyIsInBlcm1pc3Npb25zIjpbInJlYWQ6YWN0b3JzIiwicmVhZDptb3ZpZXMiXX0.aIaB27EHEh2xGOHZGWwqC3MCZ1jylkljlLZozsjNaFgaNC3Cfg4uT0CfUx9PCrtWZxEeq8-7T2_acI-KkfiAieCzYZgDYWXX2aqIiGin29Df4XpFaTQX3XycfgMcjGLyLGYEf5GRNcQpRXrdwVEbqY5cibNmDTZV27n-31vj0rSc8Z4tE8anw9uL92xlwkTL5_cBZK_RptvQHdpZ4IefABuvc90-iYr4i9F5qt-MjAbEKB_t2AeO1JLoDerVIIKxFjNtmFFJjI5ba7PV9-6vCcnha6oMq4q8xUjYiZR24eQhjvAGkblPuLNM2kGsd6t-gHJxUtQgSkJSqeLey12emQ
#DIRECTOR_TOKEN=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik41VTIycmRnRHUxbUJhTGVZQUlldCJ9.eyJpc3MiOiJodHRwczovL21vcnJpcy1kZXYudWsuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY3OGJkOWYyNWUwYzU2MjMyMWU5MjQxZiIsImF1ZCI6WyJjYXN0aW5nLWFnZW5jeSIsImh0dHBzOi8vbW9ycmlzLWRldi51ay5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzM4MDczOTIyLCJleHAiOjE3MzgwODExMjIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhenAiOiJYbHQyVEpDd05vVGo2VWJpb0VXMVc0TlpuUlJIVnhIMyIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvcnMiLCJhZGQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.eiuxID34Ys5EPH3kDCcfSN4KTdNi8sq6-QGUvqMFIAwh9jI0iX2GY1iM5u5xQiXi_SRsdF3rbYKisHZRr7n4OowvJHGwJ0HPqh92E55Oyx-DVEDGPk4lFYw63TNqch1orq7E7HHnpLMhlvgsb7Z-sGTuRe3GxFK4ilVVJ07RupsPm4w3sDTCmf6IY_ixcVp8CIDF9wQq-t9WhHOadZWd-AtKGDpXfqJZguVSCCOTbYKRasnCDRnht-AOsYo3ir3UOK-yDlOlpjVAZ-YUzFaFskHaIp26bGDp6Lhd1iinSf3VsAMMpcgU7NnLcw4enmcsRydyCxQIHs8laWAgeAQGUQ
#PRODUCER_TOKEN=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik41VTIycmRnRHUxbUJhTGVZQUlldCJ9.eyJpc3MiOiJodHRwczovL21vcnJpcy1kZXYudWsuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY3OGJkYTZkZTk3MDRlZGIxMzM3NmJhMSIsImF1ZCI6WyJjYXN0aW5nLWFnZW5jeSIsImh0dHBzOi8vbW9ycmlzLWRldi51ay5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzM4MDczOTM1LCJleHAiOjE3MzgwODExMzUsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhenAiOiJYbHQyVEpDd05vVGo2VWJpb0VXMVc0TlpuUlJIVnhIMyIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvcnMiLCJhZGQ6bW92aWVzIiwiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJyZWFkOmFjdG9ycyIsInJlYWQ6bW92aWVzIl19.Cx2Uytr71yi3iW7LnXqBQJ4OEf6PMeIA1-OvmAB1FZ2HqiFe_hr1Jz6c2JoRzKvIK-ew8sOdbQpfuTTwk9lpawykhqHagqt_KhEZ2uCKKM1R2EqFR8-Gp6FC9PVYHJWr1mGZWr48dC_K5E8-HDC-T0NPAC48HGjzozPrqKr6inweUufKnm32VPEbsZ_gk3VC_E4Qdo8Pnr22zHb-P-kcKmNKRwyuY_K7cm5irRQW9fK1v8-Ih6D0iDXaejwsQ7NC7vvBV7lY_m_oo_owkdP1EiNvxmrYzZSUzF85ERocoZZbodu_KqgdwuhAMVEQyGcQZnilNCCOEsmmdlYCb3iySw

cd /opt/render/project/src/

# Now run the migration command
flask db upgrade

echo "Setup completed successfully!"