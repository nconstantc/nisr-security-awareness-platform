"""Starter courses based on regular InfoSec mailing materials, each packaged as a separate course.

COURSES format: a list of courses, each - {title, description, chapters: [...], questions: [...]}.
questions[].chapter - the key of a chapter within that same course (chapters[].key).
"""

PASSWORDS_COURSE = {
    "title": "Password Protection Reminder",
    "description": (
        "Key requirements for the secure use and storage of credentials (logins, "
        "passwords, multi-factor authentication codes) for connecting to the Company's "
        "information systems."
    ),
    "chapters": [
        {
            "key": "main",
            "title": "Password Protection",
            "content": """
<p>The Information Security Department is issuing this reminder covering the key requirements
for the secure use and storage of credentials (logins, passwords, multi-factor
authentication codes) used to connect to the Company's information systems.</p>
<h4>Key Requirements and Recommendations</h4>
<ul>
  <li>Password length for standard user accounts - at least <strong>8 characters</strong>,
  for privileged accounts - at least <strong>12 characters</strong>; lowercase and uppercase
  letters, numbers, and special characters (%, $, @, &amp;, *, #, etc.) are required.</li>
  <li>Do not use easily guessable, dictionary passwords: names, surnames, birth dates,
  workstation names, qwerty123, 12345678, etc.</li>
  <li>Do not share passwords with other employees (including your manager, IT, or InfoSec) or
  third parties, and do not hand over control of your workstation.</li>
  <li>Do not store credentials in plain form - not on your workstation, not in notes, and not on
  paper in an accessible place.</li>
  <li>Do not send passwords in plain text, and do not send all multi-factor authentication
  components in a single message.</li>
  <li>Do not use the Company's corporate passwords for external resources (forums, online stores,
  government portals, etc.).</li>
  <li>Disable password autosave in browsers and applications.</li>
  <li><strong>Use unique passwords for different systems within the Company</strong> - using the
  same password across different internal systems is not allowed.</li>
  <li>Whenever you leave your workstation during the day - always lock the computer
  (<strong>Win + L</strong>).</li>
  <li>Administrators must change vendor default passwords (OS, applications, databases, hardware)
  before putting a system into production.</li>
</ul>
<p>If a password is compromised or suspected of being compromised - change the password immediately and notify
the Information Security Department (<strong>soc@example.com</strong>). You alone are responsible
for actions taken under your account.</p>
""",
        },
    ],
    "questions": [
        {
            "chapter": "main",
            "text": "What is the minimum password length set for a standard user account?",
            "type": "single",
            "choices": [("6 characters", False), ("8 characters", True), ("10 characters", False), ("14 characters", False)],
        },
        {
            "chapter": "main",
            "text": "What is the minimum password length set for a privileged account?",
            "type": "single",
            "choices": [("8 characters", False), ("10 characters", False), ("12 characters", True), ("16 characters", False)],
        },
        {
            "chapter": "main",
            "text": "Is it allowed to use the same password for different information systems within the Company?",
            "type": "single",
            "choices": [
                ("Yes, it's convenient", False),
                ("No, unique passwords must be used for different systems", True),
                ("Yes, if the password is complex", False),
                ("Only allowed for two systems", False),
            ],
        },
        {
            "chapter": "main",
            "text": "Who must change vendor default passwords before a system is put into production?",
            "type": "single",
            "choices": [
                ("A regular user on first login", False),
                ("Administrators", True),
                ("No one, default passwords don't need to be changed", False),
                ("The equipment manufacturer itself", False),
            ],
        },
        {
            "chapter": "main",
            "text": "What should you do when temporarily leaving your workstation during the workday?",
            "type": "single",
            "choices": [
                ("Nothing, if you're only stepping away briefly", False),
                ("Lock the computer with Win + L", True),
                ("Turn off the monitor", False),
                ("Close only your work documents", False),
            ],
        },
        {
            "chapter": "main",
            "text": "Where should you report a compromised or suspected-compromised password?",
            "type": "single",
            "choices": [
                ("Nowhere, just change the password and tell no one", False),
                ("To the Information Security Department (soc@example.com)", True),
                ("Report it a month later", False),
                ("Post it in the company's general chat", False),
            ],
        },
    ],
}

EMAIL_COURSE = {
    "title": "Reminder on Handling Incoming Email",
    "description": (
        "Warning signs to watch for when handling incoming email, "
        "so you can spot phishing and malicious messages in time."
    ),
    "chapters": [
        {
            "key": "main",
            "title": "Handling Incoming Email",
            "content": """
<p>The Information Security Department is issuing this reminder on handling incoming
email.</p>
<h4>What to Check When You Receive an Email</h4>
<ul>
  <li><strong>The sender's email address.</strong> Make sure the address is familiar and that you are
  expecting mail from this sender - pay attention to the address itself, not the display name.</li>
  <li><strong>The content of the email.</strong> If a message is flagged as coming from an external
  sender - treat it with extra caution, it may be unsafe.</li>
  <li><strong>Links that push you to click.</strong> Hover your cursor over a link (without clicking
  it!) and check its real destination - phishing links often look like real ones, but with
  altered characters.</li>
  <li><strong>Unknown attachments.</strong> Pay special attention to attachments with a double file
  extension (e.g., "report.pdf.exe"): they should not be opened or saved.</li>
  <li><strong>The sender's signature.</strong> If the signature is missing, unfamiliar, or the
  address it lists differs from the sender's address - delete the email and don't reply to it.</li>
  <li><strong>Time received.</strong> Attackers often send emails outside of business hours -
  pay attention to whether the date and time make sense.</li>
</ul>
<h4>A Few More Recommendations</h4>
<ul>
  <li>If a message is from someone unfamiliar - don't open it. If the address looks familiar but
  doesn't match exactly - also don't open it.</li>
  <li>Don't open attachments from unknown senders; pay special attention to executable files
  such as .exe, .bat, .cmd.</li>
  <li>Hyperlinks don't always lead where they claim to - they can redirect to a malicious
  site.</li>
  <li>Never provide confidential data (passwords, secret digital-signature keys) in response to
  an email requesting it.</li>
  <li>Never reply to spam.</li>
</ul>
<p>Always report any suspicious emails (phishing, malicious attachments, unknown links, spam)
to the Information Security Department (<strong>soc@example.com</strong>).</p>
""",
        },
    ],
    "questions": [
        {
            "chapter": "main",
            "text": "What should you check first when you receive an email - the sender's display name or something else?",
            "type": "single",
            "choices": [
                ("Only the sender's display name", False),
                ("The sender's actual email address", True),
                ("Only the subject line", False),
                ("It doesn't matter", False),
            ],
        },
        {
            "chapter": "main",
            "text": "What's the correct way to check where a link in an email actually leads without putting yourself at risk?",
            "type": "single",
            "choices": [
                ("Click the link and see", False),
                ("Hover your mouse over the link without clicking it", True),
                ("Forward the link to a coworker to check", False),
                ("Copy the link into a private browser window", False),
            ],
        },
        {
            "chapter": "main",
            "text": "What should you pay special attention to in email attachments?",
            "type": "single",
            "choices": [
                ("The file size", False),
                ("Double file extensions (e.g., \"report.pdf.exe\")", True),
                ("The color of the file icon", False),
                ("The language of the file name", False),
            ],
        },
        {
            "chapter": "main",
            "text": "An email's sender signature is missing or doesn't match the sender's email address. What should you do?",
            "type": "single",
            "choices": [
                ("Reply and ask who the sender is", False),
                ("Delete the email and under no circumstances reply to it", True),
                ("Forward the email to all coworkers for review", False),
                ("It's fine, continue handling the email as usual", False),
            ],
        },
        {
            "chapter": "main",
            "text": "Why is it worth paying attention to when an email was received?",
            "type": "single",
            "choices": [
                ("It has nothing to do with security", False),
                ("Attackers often send emails outside business hours - it's one sign of a fake", True),
                ("Emails always arrive on a strict schedule", False),
                ("Time received only affects mail sorting", False),
            ],
        },
        {
            "chapter": "main",
            "text": "What's the correct way to handle a spam email from an unknown sender?",
            "type": "single",
            "choices": [
                ("Reply and ask them to stop sending mail", False),
                ("Never reply to spam, delete the email", True),
                ("Forward the email to friends", False),
                ("Save the email for later", False),
            ],
        },
    ],
}

SOCIAL_ENGINEERING_COURSE = {
    "title": "Reminder on Social Engineering Methods and Required Security Measures",
    "description": (
        "Common social engineering methods (phishing, vishing, pretexting, and others) and the "
        "security measures used to defend against them."
    ),
    "chapters": [
        {
            "key": "main",
            "title": "Social Engineering Methods and Security Measures",
            "content": """
<p>Social engineering is the manipulation of people to get them to take some
action or disclose confidential information. Instead of hacking computers, attackers
trick employees into handing over information or downloading malware.</p>
<h4>Common Social Engineering Methods</h4>
<ul>
  <li><strong>Phishing.</strong> A mass mailing of fake emails impersonating a well-known company,
  asking the recipient to follow a link and enter a login/password. Spear phishing is an email
  targeted at a specific employee, apparently from management, requesting confidential data.</li>
  <li><strong>Vishing and smishing.</strong> Vishing is "voice phishing" - phone-based fraud
  (for example, an attacker posing as a support technician). Smishing has the same goal, but
  is carried out via SMS messages.</li>
  <li><strong>Pretexting.</strong> An attacker uses a fabricated pretext (cover story) to
  get a victim to disclose information - for example, posing as an auditor or a survey
  participant.</li>
  <li><strong>Trojan.</strong> A bait email promises quick profit or a prize, but the result is
  a virus getting onto the computer. It's often disguised as ordinary internal correspondence.</li>
  <li><strong>"Baiting" ("road apple").</strong> An infected physical drive (USB) with the company's
  logo is left in a public place (a parking lot, a cafeteria) hoping curiosity will lead
  whoever finds it to plug it in.</li>
  <li><strong>Reverse social engineering.</strong> An attacker sets up a situation in advance (for example,
  warning of a "possible software failure") so that the victim reaches out to them for "help" and
  hands over the needed information on their own.</li>
</ul>
<h4>Security Measures</h4>
<ul>
  <li><strong>Verify the source.</strong> Don't trust a message blindly: compare the sender's
  address with previous emails, hover over links without clicking them, and check
  the spelling.</li>
  <li><strong>Verify identity.</strong> Don't let strangers in on your badge,
  ask for the caller's name and position, and verify that information through official
  sources.</li>
  <li><strong>Stop and think.</strong> Don't rush to share data - it's better to call back on an
  official number or write to an official address to verify the source's
  legitimacy.</li>
  <li><strong>Don't rush.</strong> A false sense of urgency is a standard trick used by scammers. Take a pause,
  say you'll verify the information, and call back.</li>
</ul>
<p>Report any suspicious emails and contacts to the Information Security Department
(<strong>soc@example.com</strong>).</p>
""",
        },
    ],
    "questions": [
        {
            "chapter": "main",
            "text": "What is social engineering?",
            "type": "single",
            "choices": [
                ("A technical method of hacking servers without any human involvement", False),
                ("Manipulating people to get them to hand over information or take actions the attacker wants", True),
                ("An official employee training methodology", False),
                ("A type of antivirus software", False),
            ],
        },
        {
            "chapter": "main",
            "text": "What is \"voice phishing\" - phone-based fraud aimed at extracting data - called?",
            "type": "single",
            "choices": [("Smishing", False), ("Pretexting", False), ("Vishing", True), ("Trojan", False)],
        },
        {
            "chapter": "main",
            "text": "An attacker poses as an auditor and asks for internal data under a fabricated pretext. What is this method called?",
            "type": "single",
            "choices": [("Pretexting", True), ("Smishing", False), ("Baiting (\"road apple\")", False), ("Reverse social engineering", False)],
        },
        {
            "chapter": "main",
            "text": "Someone \"accidentally leaves\" a USB drive with the company logo and the label \"Employee Salaries\" in the company parking lot. What is this attack called?",
            "type": "single",
            "choices": [("Vishing", False), ("Baiting (\"road apple\")", True), ("Pretexting", False), ("Phishing", False)],
        },
        {
            "chapter": "main",
            "text": "Someone calls, claims to be from the information security team, and urgently asks you to read out your password. What should you do?",
            "type": "single",
            "choices": [
                ("Give the password right away, since they said they're calling from InfoSec", False),
                ("Refuse, call back on the InfoSec team's official number from the company directory, and verify", True),
                ("Read out only part of the password", False),
                ("Ask them to call back later and give it then", False),
            ],
        },
        {
            "chapter": "main",
            "text": "Attackers create a sense of urgency and pressure you to provide data immediately. What's the correct response?",
            "type": "single",
            "choices": [
                ("Act quickly so as not to let the company down", False),
                ("Stop, don't rush, and verify the source of the request before sharing anything", True),
                ("Share part of the data to satisfy the request", False),
                ("Ignore it, but don't report it to InfoSec either", False),
            ],
        },
    ],
}

GENERAL_REQUIREMENTS_COURSE = {
    "title": "Reminder of Key Information Security Requirements",
    "description": (
        "A summary reminder of key InfoSec requirements: password protection, antivirus protection, "
        "corporate email, internet use, remote access (VPN), and the physical security "
        "of workstations."
    ),
    "chapters": [
        {
            "key": "passwords",
            "title": "Password Protection",
            "content": """
<ul>
  <li>Never share your password with anyone else, including coworkers, managers, or IT and
  InfoSec staff.</li>
  <li>Don't store passwords in plain form: in notes, files on a computer, or on paper in
  accessible places.</li>
  <li>Don't send passwords by email, messengers, or other unsecured channels; don't send
  all your login details (login, password, MFA code) in a single message.</li>
  <li>Use different passwords for different systems within the Company.</li>
  <li>Don't use corporate passwords for external resources (personal email, internet services,
  etc.).</li>
  <li>Disable password autosave in browsers and applications.</li>
  <li>Password length: at least 8 characters for standard accounts, at least 12 for
  privileged accounts; lowercase and uppercase letters, numbers, and special characters are required.</li>
  <li>Don't use simple, predictable passwords (names, birth dates, "qwerty", "123456").</li>
  <li>If you suspect a password has been compromised - change it immediately and notify InfoSec.</li>
</ul>
""",
        },
        {
            "key": "antivirus",
            "title": "Antivirus Protection",
            "content": """
<ul>
  <li>Don't disable or change the settings of your installed antivirus.</li>
  <li>Scan USB drives for viruses before use.</li>
  <li>If you suspect a virus infection, notify InfoSec immediately.</li>
</ul>
""",
        },
        {
            "key": "email",
            "title": "Corporate Email",
            "content": """
<ul>
  <li>Sending confidential information to external recipients without approval is prohibited.</li>
  <li>Confidential data may only be sent in encrypted form.</li>
  <li>Don't forward work emails to your personal email.</li>
  <li>Don't open attachments or click links in emails from unknown senders.</li>
  <li>Don't use your corporate email for personal purposes, subscriptions, or mass mailings without
  approval.</li>
  <li>Don't send messages on behalf of other users (including by spoofing the address).</li>
  <li>Don't take part in distributing illegal content.</li>
  <li>If you receive a suspicious or phishing email - notify InfoSec immediately.</li>
</ul>
""",
        },
        {
            "key": "internet",
            "title": "Internet",
            "content": """
<ul>
  <li>Don't transmit confidential information in plain form.</li>
  <li>Respect copyright and the law when downloading materials.</li>
  <li>Don't post or distribute content containing threats, insults, or illegal
  material.</li>
  <li>Don't download files or programs that could harm the information system.</li>
  <li>Don't use anonymizers, proxy servers, or other tools to bypass restrictions.</li>
  <li>Limit downloading files unrelated to work.</li>
  <li>Don't click suspicious links or ad banners.</li>
</ul>
""",
        },
        {
            "key": "vpn",
            "title": "Remote Access (VPN)",
            "content": """
<p>Employees using remote access (VPN) to connect to the Company's corporate network
must comply with the following requirements:</p>
<ul>
  <li>Use VPN only for work and within the scope of your job duties.</li>
  <li>Prevent unauthorized people from accessing your workstation.</li>
  <li>Never share your connection credentials with anyone.</li>
  <li>End the VPN connection once you're done working.</li>
  <li>Don't use public Wi-Fi networks to connect.</li>
  <li>If working from a personal device - install antivirus software on it.</li>
</ul>
""",
        },
        {
            "key": "physical",
            "title": "Physical Security (PC Tamper Seals)",
            "content": """
<p>To physically protect personal computers from unauthorized access, a
tamper-seal procedure is used - a sealing sticker is applied to the PC case.</p>
<ul>
  <li>Don't damage or remove the tamper-seal sticker on your computer.</li>
  <li>Check that the seal is intact. Using a PC without an intact seal is prohibited.</li>
  <li>If you notice a damaged seal, immediately notify IT and InfoSec.</li>
</ul>
<p>Violations of information security requirements are subject to liability under
the Company's internal regulatory documents and the laws of the Republic of
Kazakhstan. Report all InfoSec incidents to <strong>soc@example.com</strong>.</p>
""",
        },
    ],
    "questions": [
        {
            "chapter": "passwords",
            "text": "Is it allowed to use the same password for multiple systems within the Company?",
            "type": "single",
            "choices": [
                ("Yes, it makes it easier to remember", False),
                ("No, different systems require different passwords", True),
                ("Yes, if the password is complex", False),
                ("Allowed for no more than two systems", False),
            ],
        },
        {
            "chapter": "passwords",
            "text": "Where should you report a suspected password compromise?",
            "type": "single",
            "choices": [
                ("Nowhere, just change the password", False),
                ("To the Information Security Department (InfoSec)", True),
                ("Report it at the end-of-month meeting", False),
                ("To the HR department", False),
            ],
        },
        {
            "chapter": "antivirus",
            "text": "What should you do before using a USB drive on a work computer?",
            "type": "single",
            "choices": [
                ("Open the files right away", False),
                ("Scan the drive for viruses", True),
                ("Format the drive", False),
                ("Nothing, USB drives are safe", False),
            ],
        },
        {
            "chapter": "antivirus",
            "text": "Is a user allowed to disable or change the settings of installed antivirus software?",
            "type": "single",
            "choices": [
                ("Yes, if it's getting in the way of work", False),
                ("No, this is prohibited", True),
                ("Yes, with a coworker's agreement", False),
                ("Yes, but only temporarily", False),
            ],
        },
        {
            "chapter": "email",
            "text": "Is it allowed to forward work emails to a personal email address?",
            "type": "single",
            "choices": [
                ("Yes, if you need to work from home", False),
                ("No, this is prohibited", True),
                ("Yes, if the email has no attachments", False),
                ("Allowed once a week", False),
            ],
        },
        {
            "chapter": "email",
            "text": "In what form can confidential data be sent by email to external recipients?",
            "type": "single",
            "choices": [
                ("In plain form, if the recipient is trusted", False),
                ("Only in encrypted form and with prior approval", True),
                ("Confidential data can always be sent without restriction", False),
                ("Only using the sender's personal email", False),
            ],
        },
        {
            "chapter": "internet",
            "text": "Is it allowed to use anonymizers and proxy servers to bypass internet usage restrictions?",
            "type": "single",
            "choices": [
                ("Yes, if it speeds up work", False),
                ("No, this is prohibited", True),
                ("Allowed with a manager's permission", False),
                ("Allowed only for work tasks", False),
            ],
        },
        {
            "chapter": "vpn",
            "text": "Is it allowed to connect to the corporate VPN over public Wi-Fi networks?",
            "type": "single",
            "choices": [
                ("Yes, it's convenient while traveling", False),
                ("No, using public Wi-Fi networks for VPN is prohibited", True),
                ("Allowed if the network is password-protected", False),
                ("Allowed only in airports", False),
            ],
        },
        {
            "chapter": "vpn",
            "text": "What should you do once you're done working over VPN?",
            "type": "single",
            "choices": [
                ("Nothing, the connection can stay active", False),
                ("End the VPN connection", True),
                ("Leave the connection open until the next day", False),
                ("Hand off the session to a coworker", False),
            ],
        },
        {
            "chapter": "physical",
            "text": "What should you do if you notice a damaged tamper-seal sticker on a computer?",
            "type": "single",
            "choices": [
                ("Keep working as usual", False),
                ("Immediately notify IT and InfoSec", True),
                ("Patch the damage yourself", False),
                ("Report it a month later", False),
            ],
        },
        {
            "chapter": "physical",
            "text": "Is it allowed to use a personal computer without a tamper-seal sticker, or with a damaged seal?",
            "type": "single",
            "choices": [
                ("Yes, if the computer works fine", False),
                ("No, using a PC without an intact seal is prohibited", True),
                ("Allowed for one workday", False),
                ("Allowed with a manager's verbal consent", False),
            ],
        },
    ],
}

COURSES = [PASSWORDS_COURSE, EMAIL_COURSE, SOCIAL_ENGINEERING_COURSE, GENERAL_REQUIREMENTS_COURSE]
