export AUTH0_DOMAIN=morris-dev.uk.auth0.com
export ALGORITHMS='RS256'
export AUTH0_API_AUDIENCE=casting-agency

#local database url
export LOCAL_DATABASE_URL='postgresql://drive:postgres@localhost:5432/casting_agency'

#heroku database url
export RENDER_DATABASE_URL='postgresql://casting_agency_w2mb_user:HOYwJAuTXdtFGx8NnhoRhbVJcRmOsTL8@dpg-cu41ugtds78s73cgnlh0-a/casting_agency_w2mb'
#JWTS for all the 3 roles/users:
export ASSISTANT_TOKEN=
export DIRECTOR_TOKEN=
export PRODUCER_TOKEN=