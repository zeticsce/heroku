<a href="https://www.codacy.com/gh/coddrago/Heroku/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=coddrago/Heroku&amp;utm_campaign=Badge_Grade"><img src="https://app.codacy.com/project/badge/Grade/97e3ea868f9344a5aa6e4d874f83db14"/></a>
<a href="#"><img src="https://img.shields.io/github/languages/code-size/coddrago/Heroku"/></a>
<a href="#"><img src="https://img.shields.io/github/issues-raw/coddrago/Heroku"/></a>
<a href="#"><img src="https://img.shields.io/github/license/coddrago/Heroku"/></a>
<a href="#"><img src="https://img.shields.io/github/commit-activity/m/coddrago/Heroku"/></a><br>
<a href="#"><img src="https://img.shields.io/github/forks/coddrago/Heroku?style=flat"/></a>
<a href="#"><img src="https://img.shields.io/github/stars/coddrago/Heroku"/></a>&nbsp;<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a><br>

### Disclaimer

> Even though Heroku has extended security measures for scam-modules protection, flood-based account restrictions protection and others, it still may cause damage to server / account if you install module from untrusted developer. Please, consider downloading modules exceptionally from official repository or from trusted developers. If you are not sure about whether module is safe or not, please, DO NOT INSTALL IT. Same goes for unknown commands (.terminal, .e, .eval, .ec, .ecpp, etc.). You have been warned.

<hr>
<h2><img src="https://github.com/hikariatama/assets/raw/master/1326-command-window-line-flat.webp" height="54" align="middle"> Installation</h2>

<b>Manual installation (for VDS/VPS server):</b><br>
<code>apt update && apt install git python3 -y && git clone https://github.com/coddrago/Heroku && cd Heroku && pip install -r requirements.txt && python3 -m heroku</code><br.>
<i>If you are on VPS\VDS, type <code>--proxy-pass</code> in the end of command to open SSH tunnel to your Heroku web interface, or use <code>--no-web</code> to complete setup in console</i><br>
<br>
<b>Some further details:</b>

<details>
 <summary>Pre-installed automatic database backuper</summary>
 <img src="https://user-images.githubusercontent.com/36935426/202905566-964d2904-f3ce-4a14-8f05-0e7840e1b306.png" width="300">
</details>
<details>
 <summary>Welcome installation info</summary>
 <img src="https://user-images.githubusercontent.com/36935426/202905720-6319993b-697c-4b09-a194-209c110c79fd.png" width="300">
 <img src="https://user-images.githubusercontent.com/36935426/202905746-2a511129-0208-4581-bb27-7539bd7b53c9.png" width="300">
</details>

<hr>
<h2><img src="https://github.com/hikariatama/assets/raw/master/35-edit-flat.webp" height="54" align="middle"> Changes</h2>

<ul>
 <li>🆕 <b>Latest Telegram layer</b> with forums and other stuff</li>
 <li>🔓 <b>Security</b> improvements, including <b>native entity caching</b> and <b>targeted security rules</b></li>
 <li>🎨 <b>UI/UX</b> improvements</li>
 <li>📼 Improved and new <b>core modules</b></li>
 <li>⏱ Quick <b>bug fixes</b> (compared to official FTG and GeekTG)</li>
 <li>▶️ <b>Inline forms, galleries and lists</b></li>
 <li>🔁 <b>Backward compatibility</b> with FTG, GeekTG and Hikka modules</li>
</ul>
<hr>
<h2 border="none"><img src="https://github.com/hikariatama/assets/raw/master/1312-micro-sd-card-flat.webp" height="54" align="middle"> Requirements</h2>
<ul>
 <li>Python 3.9-3.13</li>
 <li>API_ID and HASH from <a href="https://my.telegram.org/apps" color="#2594cb">Telegram</a></li>
</ul>
<hr>
<h2 border="none"><img src="https://github.com/hikariatama/assets/raw/master/680-it-developer-flat.webp" height="54" align="middle"> Documentation</h2>

Check out <a href="https://heroku-ub.xyz/">heroku-ub.xyz</a> for users' documentation<br>
And <a href="https://dev.heroku-ub.xyz/">dev.heroku-ub.xyz</a> for developers documentation

<hr>
<h2 border="none"><img src="https://github.com/hikariatama/assets/raw/master/981-consultation-flat.webp" height="54" align="middle"> <a href="https://t.me/heroku_talks">Support</a></h2>

<hr>
<i>⚠️ This project is provided as-is. Developer doesn't take ANY responsibility over any problems, caused by userbot. By installing Heroku you take all risks on you. This is but not limited to account bans, deleted (by Telegram algorithms) messages, SCAM-modules, leaked sessions (due to SCAM-modules). It is <b>highly</b> recommended to enable the API Flood protection (.api_fw_protection) and not to install many modules at once. By using Heroku you give your consent to any actions made by your account in background in purposes of automatization. Please, consider reading https://core.telegram.org/api/terms for more information.</i>

<b>Special thanks to:</b>

<ul>
    <li><a href="https://gitlab.com/hikariatama">Hikari</a> for Hikka, which is the base of project</li>
    <li><a href="https://t.me/lonami">Lonami</a> for Telethon, which is the base of Heroku-TL</li>
</ul>