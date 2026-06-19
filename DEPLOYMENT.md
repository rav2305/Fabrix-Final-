# Fabrix Admin Panel - Deployment Guide

This guide details the exact steps to make your Fabrix Admin Panel live on the internet, secure it, and access it from your mobile phone.

---

## 1. Make GitHub Repository Private (Security First)
Since this admin panel contains store sales, costs, customer data, and login portals, it is critical that the codebase is private:
1. Log in to your GitHub account and navigate to: `https://github.com/rav2305/Fabrix-Final-`
2. Click on the **Settings** tab (the gear icon on the top nav bar of the repository).
3. Scroll all the way down to the **Danger Zone** section.
4. Click the **Change visibility** button next to *Change repository visibility*.
5. Select **Make private** and follow the confirmation prompts.

---

## 2. Deploying to Hostinger

Choose the section below that matches your Hostinger plan.

### Option A: Hostinger Shared Hosting (Using hPanel "Setup Python App")
Most Hostinger plans (Premium, Business) are shared hosting. They run Python web apps using Phusion Passenger.

1. **Log in to hPanel**: Go to [Hostinger hPanel](https://hpanel.hostinger.com).
2. **Access Python App Settings**:
   * Navigate to your **Website Dashboard**.
   * Under the **Advanced** section in the left sidebar, click on **Setup Python App**.
3. **Configure the App**:
   * **Python Version**: Select `3.10` or higher.
   * **Application root**: Enter `public_html` or the folder name where your files will reside (e.g. `fabrix`).
   * **Application URL**: Select your domain (e.g. `yourdomain.com`).
   * **Application startup file**: Enter `passenger_wsgi.py`.
   * Click **Create**.
4. **Upload your Code**:
   * Use hPanel's **File Manager** or Git to upload all project files (except `venv/` and `__pycache__/` which are ignored) directly to the application root directory you specified.
   * Ensure `app.py`, `models.py`, `requirements.txt`, `passenger_wsgi.py`, and the `templates/`/`static/` directories are uploaded.
5. **Install Dependencies**:
   * Once files are uploaded, go back to **Setup Python App** in hPanel.
   * Find the **Configuration files** section, enter `requirements.txt`, and click **Add**.
   * Click the **Run Pip Install** button next to `requirements.txt`. Hostinger will automatically download and install `Flask`, `pandas`, `openpyxl`, etc.
6. **Start the App**:
   * Scroll to the top and click **Restart Application**.
   * Open your browser and go to `yourdomain.com`. The Fabrix Admin login page should appear.

---

### Option B: Hostinger VPS (Virtual Private Server)
If you have a Linux VPS (Ubuntu 20.04/22.04/24.04), you have full root control. Here is the standard production setup.

1. **SSH into your VPS**:
   ```bash
   ssh root@your_vps_ip
   ```
2. **Install system packages**:
   ```bash
   sudo apt update
   ```
   * *If Python is not installed (e.g., Python 3.10+):*
   ```bash
   sudo apt install -y python3-pip python3-venv git nginx
   ```
3. **Clone the code**:
   ```bash
   cd /var/www
   git clone https://github.com/rav2305/Fabrix-Final-.git fabrix
   cd fabrix
   ```
4. **Set up virtual environment & dependencies**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. **Set up Systemd Service (Gunicorn)**:
   * Create a service file:
     ```bash
     sudo nano /etc/systemd/system/fabrix.service
     ```
   * Paste the following configuration:
     ```ini
     [Unit]
     Description=Fabrix Flask Admin Daemon
     After=network.target

     [Service]
     User=www-data
     Group=www-data
     WorkingDirectory=/var/www/fabrix
     Environment="PATH=/var/www/fabrix/venv/bin"
     ExecStart=/var/www/fabrix/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 app:app

     [Install]
     WantedBy=multi-user.target
     ```
   * Save and close (`Ctrl+O`, `Enter`, `Ctrl+X`).
   * Start and enable the service:
     ```bash
     sudo systemctl start fabrix
     sudo systemctl enable fabrix
     ```

6. **Configure Nginx Reverse Proxy**:
   * Open a new Nginx server block:
     ```bash
     sudo nano /etc/nginx/sites-available/fabrix
     ```
   * Paste the configuration (replace `yourdomain.com` with your Hostinger domain):
     ```nginx
     server {
         listen 80;
         server_name yourdomain.com www.yourdomain.com;

         location / {
             proxy_pass http://127.0.0.1:8000;
             proxy_set_header Host $host;
             proxy_set_header X-Real-IP $remote_addr;
             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
             proxy_set_header X-Forwarded-Proto $scheme;
         }

         location /static {
             alias /var/www/fabrix/static;
         }
     }
     ```
   * Enable the site and restart Nginx:
     ```bash
     sudo ln -s /etc/nginx/sites-available/fabrix /etc/nginx/sites-enabled/
     sudo nginx -t
     sudo systemctl restart nginx
     ```
7. **Obtain SSL (HTTPS) via Let's Encrypt**:
   ```bash
   sudo apt install -y certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

---

## 3. Running/Accessing from your Phone

Once deployed on Hostinger:
1. **Access Domain**: Simply open Chrome, Safari, or any browser on your smartphone and navigate to `https://yourdomain.com`.
2. **Responsive Mobile UI**: The layout collapses automatically into a clean mobile layout:
   * Navigation links tuck into a gold slide-out sidebar toggled by a burger icon.
   * Tables become scrollable horizontally.
   * Popups/modals center on the screen.
3. **Sharing Invoices**:
   * Click **New Invoice** on your phone.
   * Fill out customer details and select items.
   * Click **Generate Invoice**.
   * Click **Share on WhatsApp**. The app will automatically launch the WhatsApp application on your phone with the formatted text message ready to send to the client!
4. **Print Invoices**:
   * On mobile, clicking **Print Invoice** opens the phone's native print screen (AirPrint on iOS / Google Print on Android).
   * From there, you can choose "Print" to a wireless receipt printer, or click "Save as PDF" to save it directly to your phone.

---

## 4. Default Credentials (First-Time Login)
On first startup, the database automatically seeds a secure administrator user.
* **Username**: `admin`
* **Password**: `admin123`
* **Role**: `admin`

> [!IMPORTANT]
> Immediately upon logging in for the first time, navigate to the **User Access** section, create your personalized administrator account, log into it, and delete the default `admin` profile to secure your shop.
