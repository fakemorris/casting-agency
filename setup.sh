#!/bin/bash

# Ensure your environment is correctly set up

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (if you're not using Render's dashboard to do this)
export AUTH0_DOMAIN="morris-dev.uk.auth0.com"
export ALGORITHMS="RS256"
export AUTH0_API_AUDIENCE="casting-agency"

# Local database URL (you can skip this if Render handles it)
export LOCAL_DATABASE_URL="postgresql://drive:postgres@localhost:5432/casting_agency"

# Database URL for Render (ensure you're getting this from the Render environment variables)
export RENDER_DATABASE_URL="postgresql://casting_agency_w2mb_user:HOYwJAuTXdtFGx8NnhoRhbVJcRmOsTL8@dpg-cu41ugtds78s73cgnlh0-a/casting_agency_w2mb"

# JWT tokens for different roles (you'll need to securely fetch these from the Render environment or elsewhere)
export ASSISTANT_TOKEN="your_assistant_jwt_token_here"
export DIRECTOR_TOKEN="your_director_jwt_token_here"
export PRODUCER_TOKEN="your_producer_jwt_token_here"

echo "Setup completed successfully!"