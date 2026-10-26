FROM astrocrpublic.azurecr.io/runtime:3.3-11

# Keep the Astro Runtime version generated for your project.

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
