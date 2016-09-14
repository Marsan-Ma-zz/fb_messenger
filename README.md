# Minimum Facebook ChatBot App

A facebook chatbot (messenger) backend server, written in python flask framework


## Deploy Steps

Take a glimpse on [facebook official tutorial](https://developers.facebook.com/docs/messenger-platform/quickstart), then start wondering:   

1. How to get some free and workable SSL certificate?
2. What the heck about these tokens?



## Free Workable SSL certification!

Facebook don't accept self-signed SSL key, but SSL certificate from trusted source is not free, usually like $50/yr at least.

Thanks to guys from [ISRG (Internet Security Research Group)](https://letsencrypt.org/isrg/), we have [free ssl certificate](https://letsencrypt.org/) that accepted by main-stream browsers, and most important --- accepted by Facebook!

You could follow the official tutorial from [let's encrypt](https://letsencrypt.org/getting-started/), or inshort, just type:

      wget https://dl.eff.org/certbot-auto
      chmod a+x certbot-auto
      ./certbot-auto certonly --standalone -d <your.domain.name>

Then your keys are available in `/etc/letsencrypt/live`, yay!  
(Note that port 443 (https) should not blocked by firewall, else can't be verified.)

Then you need to copy this two key file into you ssl folder:

    cp /etc/letsencrypt/live/fullchain1.pem  fb_messenger/ssl/server.crt
    cp /etc/letsencrypt/live/privkey1.pem  fb_messenger/ssl/server.key



## Creating Facebook App, and the Tokens

There are two tokens matters here:

* The `VERIFY_TOKEN` for facebook to verify that **YOU OWN THE DOMAIN**, this token will only used once. And you will fill-in whatever you like in this step:
![the VERIFY_TOKEN](https://scontent-tpe1-1.xx.fbcdn.net/t39.2178-6/12057143_211110782612505_894181129_n.png)

And you will fill the same in `config.yaml`
You can't pass the `Verify and Save` button because once you click it, facebook will try to access your site and make sure: 

1. you have SSL certificate ready 
2. you have token setup ready

We will come back later and click this darn button later, after we settle everything...



* The `FACEBOOK_TOKEN` for sending message on behalf of your certain facebook fanpage, which you get it from this step:
![the FACEBOOK_TOKEN](https://scontent-tpe1-1.xx.fbcdn.net/t39.2178-6/12995543_1164810200226522_2093336718_n.png)

Also, you will fill the same in `config.yaml`




## Finally, start your server!

You need to start your server by `python3 app.py`, and make sure it's public accessible by Facebook to verify your SSL is working! 

Now we could go back to the **webhook** part, click this `Verify and Save` button and see it done!

#### Enjoy the chatting with your bot!
