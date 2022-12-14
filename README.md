# Overview

An attempt to disprove the [efficient market hypothesis](https://en.wikipedia.org/wiki/Efficient-market_hypothesis). There are many models out there, without much statistics backing them up. So we will test and confirm the validaty of them all. Here is some information:

* [Jim Simmons](https://en.wikipedia.org/wiki/Jim_Simons_(mathematician))
  * [Renaissance Technology](https://en.wikipedia.org/wiki/Renaissance_Technologies#Medallion_Fund)
* [Fama French three-factor model](https://en.wikipedia.org/wiki/Fama%E2%80%93French_three-factor_model) 
* [Carhart four-factor model](https://en.wikipedia.org/wiki/Carhart_four-factor_model)
* [Universal Portfolio](https://isl.stanford.edu/~cover/papers/paper93.pdf)
* [Modern Portfolio Theory](https://en.wikipedia.org/wiki/Modern_portfolio_theory)
* [Efficient Frontier](https://en.wikipedia.org/wiki/Efficient_frontier)
* [Post-Modern Portfolio Theory](https://en.wikipedia.org/wiki/Post-modern_portfolio_theory)
* [Markowitz Model](https://en.wikipedia.org/wiki/Markowitz_model)
* [Black Litterman Model](https://en.wikipedia.org/wiki/Black%E2%80%93Litterman_model)
* [Black Scholes Model](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model)
* [RBF Kernels](https://en.wikipedia.org/wiki/Radial_basis_function_kernel)
* [Long Short Term Memory Neural Networks](https://en.wikipedia.org/wiki/Long_short-term_memory)
### High Frequency Trading (HFT)
* [Order Flow Imbalance](https://dm13450.github.io/2022/02/02/Order-Flow-Imbalance.html)
* [The price impact of order book events](https://arxiv.org/pdf/1011.6402.pdf)
* [Evaluating trade classification algorithms: Bulk volume classification versus the tick rule and the Lee-Ready algorithm](https://www.sciencedirect.com/science/article/abs/pii/S1386418115000415)


## Front End
### ReactJS
Install cURL with: 

    sudo apt install curl

Install nvm, with: 

    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash
    
Install the current stable LTS release of Node.js along with npm: 

    nvm install --lts
    
Install react scripts:

    npm install react-scripts
    
Inside the root of the web app, start the web application with:

    npm start

### React developer tools
Add the react developer tools extension to your browser to add the 'Components' tab to the browser developer tools. This provides inspection of different components in a tree structure.

:bulb: **Tip:** `Ctrl + Shift + I` opens up the developer tools on a webpage.

## Back End
Either Django, Flask, or FastAPI

## Database
### MySQL

#### Install MySQL:

    sudo apt install mysql-server

Confirm it installed successfully and is active:

    systemctl status mysql

Connect to MySQL Server with the client:

    sudo mysql -u root 

#### Set a password for root:

Log in as root:

    sudo mysql -u root
    
Add a password for root, replacing `<password>` with your password:

    ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '<password>'; 

Log out of MySQL by executing `exit;` then restart the MySQL service:

    sudo service mysql restart

## Account Management
