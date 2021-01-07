crypto_data = None # We will reuse this object everytime we render the homepage.
# You can also decide not to reuse it, but we'll have to think about API request limitation 
# and on top of that, having it cached will make it render faster

@app.route("/") # Tell the server to use this function when '/' is the url
def main():
    global crypto_data
    if crypto_data is None: # If crypto_data is not yet defined, make the API request
        crypto_data = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?sort=market_cap&start=1&cryptocurrency_type=tokens&convert=BTC', headers={'X-CMC_PRO_API_KEY': '37d49a04-de45-445f-b473-fa22982fdc5d'}) # Replace YOUR_API_KEY with the key in your account
        crypto_data = crypto_data.json() # Transform the received data into JSON so we can use it
    return render_template('index.html', crypto_data=crypto_data) # Render the html