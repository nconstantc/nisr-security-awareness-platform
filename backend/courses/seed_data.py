"""Initial information security course - edited further via the Django Admin."""

COURSE_TITLE = "Information Security Briefing 2025"
COURSE_DESCRIPTION = (
    "Mandatory information security briefing for all employees of the Organization. "
    "Covers InfoSec policy, password security, workstation protection, internet "
    "safety, and email use."
)

CHAPTERS = [
    {
        "key": "policy",
        "title": "Information Security Policy",
        "content": """
<p>An information security policy is a set of documented rules, procedures,
practical methods, and guidelines in the field of information security that
the Organization follows in its activities.</p>
<p>Every employee affects information security and bears personal responsibility for
meeting the requirements of the InfoSec Policy:</p>
<ul>
  <li><strong>Managers</strong> - are responsible for communicating InfoSec requirements to employees and
  monitoring their compliance.</li>
  <li><strong>Employees</strong> - are personally responsible for meeting InfoSec requirements.</li>
</ul>
<p>The key internal regulatory documents are mandatory reading and compliance for all
employees: the Information Security Policy; Rules for Using the Internet, Email,
and Remote Access (VPN); the Workstation Security Procedure; Password
Management Rules; the Account and Access Rights Management Procedure; Antivirus
Protection Rules; InfoSec Incident Management Rules; the Confidential Information Policy.</p>
<h4>Procedure for Reporting InfoSec Violations (Incidents)</h4>
<p>If you have identified an information security incident, have information about one, or
have a suspicion - you must immediately report it to the Information Security
Department. The Organization guarantees confidentiality and a thorough review of the report, and
also guarantees that you will not be subjected to discrimination, dismissal, or other retaliation for
reporting, regardless of whether the violation is confirmed.</p>
""",
    },
    {
        "key": "passwords",
        "title": "Password Security",
        "content": """
<p>Password protection is the first step in securing information on a computer. A password protects
against unauthorized access and against some malware attempting to gain access over the
network.</p>
<h4>Users are prohibited from</h4>
<ul>
  <li>Sharing passwords with other employees (including their manager) and third parties.</li>
  <li>Storing logins/passwords in plain form: in notebooks, text files, or on paper in an
  accessible place.</li>
  <li>Sending passwords in plain text, or sending all multi-factor authentication components
  in a single message.</li>
  <li>Saving passwords in the browser - decline the browser's offer and uncheck
  "remember me".</li>
  <li>Using the same password for work accounts and external resources (forums,
  online stores, etc.).</li>
</ul>
<h4>Users must</h4>
<p>If a password is compromised or suspected of being compromised - immediately change the password and notify the
IT and InfoSec Departments. You alone are responsible for actions taken under
your account.</p>
<h4>Password Complexity Requirements</h4>
<ul>
  <li>At least <strong>8 characters</strong> for standard user accounts.</li>
  <li>At least <strong>12 characters</strong> for privileged accounts.</li>
  <li>Lowercase and uppercase letters, numbers, and special characters are required.</li>
  <li>Dictionary words or easily guessable passwords (names, birth dates, qwerty123, etc.)
  must not be used.</li>
</ul>
<p>The best way to "store" a password is to memorize it: that way it can't be stolen or spied on.</p>
""",
    },
    {
        "key": "workstation",
        "title": "Workstation Protection",
        "content": """
<p>If an attacker gains access to a single computer, they can harm the entire system. The main
threat is malware, which can infiltrate a computer in various ways, so the antivirus
must always be functioning correctly.</p>
<h4>Users are prohibited from</h4>
<ul>
  <li>Changing the settings or configuration of antivirus protection, or removing or disabling it.</li>
  <li>Installing unlicensed software or software unrelated to work.</li>
  <li>Independently installing software if this is not part of their job duties.</li>
  <li>Connecting USB drives and other external media not approved by the InfoSec Department.</li>
</ul>
<h4>Users must</h4>
<ul>
  <li>Scan external storage media for viruses before use.</li>
  <li>Lock the computer when leaving their workstation (<strong>Win + L</strong>).</li>
  <li>Notify IT and InfoSec of any suspected virus infection.</li>
</ul>
<p>Signs of infection: unexpected messages and sounds; programs launching on their own;
changes to browser settings or the home page; the antivirus being blocked or disabled; strange
icons in the taskbar.</p>
""",
    },
    {
        "key": "internet",
        "title": "Internet Safety",
        "content": """
<p>New malicious websites appear online every day. Attackers use eye-catching
news hooks, ads, and pop-ups to lure users and install malware
"in addition to" the promised content.</p>
<h4>Users are prohibited from</h4>
<ul>
  <li>Visiting resources unrelated to work, as well as those that violate the law.</li>
  <li>Disclosing the Organization's confidential information.</li>
  <li>Downloading/distributing pirated content, viruses, or security bypass tools.</li>
  <li>Running files downloaded from the internet without first scanning them with an antivirus.</li>
</ul>
<h4>Users must</h4>
<ul>
  <li>Check the exact spelling of a website's address - for example, "example.com" and "exarnple.com" are
  different sites.</li>
  <li>Check for a valid security certificate (the address should start with
  <code>https://</code>). If the browser warns that the certificate is not trusted -
  close the site and do not proceed.</li>
  <li>Not click on ad banners, and not agree to pop-up offers or
  prizes/giveaways for contests they never entered.</li>
  <li>Only download files from trusted sites.</li>
</ul>
""",
    },
    {
        "key": "email",
        "title": "Email",
        "content": """
<p>Corporate email is a common channel for spreading malware: attackers spoof the
sender's address with similar-looking domains, attach viruses to attachments, and run phishing attacks
asking for confidential data.</p>
<h4>Users are prohibited from</h4>
<ul>
  <li>Sending emails on behalf of another user (including by spoofing the address).</li>
  <li>Using their work email for personal purposes or unrelated mailing lists.</li>
  <li>Sending confidential information to external email addresses (mail.ru, gmail.com, etc.).</li>
  <li>Clicking links or opening attachments from unknown senders.</li>
  <li>Participating in forwarding "chain letters" ("good luck" emails).</li>
  <li>Sending logins/passwords by email in plain text.</li>
</ul>
<h4>Users must</h4>
<ul>
  <li>Check the recipient's address before sending; when receiving mail - carefully
  check the sender's address.</li>
  <li>Be cautious with hyperlinks and attachments, especially ones with double file extensions
  (for example, "report.pdf.exe").</li>
  <li>Report any suspicious emails to the InfoSec Department: phishing, unknown attachments,
  or suspicious links.</li>
  <li>Never reply to spam or provide confidential data in response to an email requesting
  it.</li>
</ul>
""",
    },
]

QUESTIONS = [
    # --- policy ---
    {
        "chapter": "policy",
        "text": "Who bears personal responsibility for meeting the requirements of the Information Security Policy?",
        "type": "single",
        "choices": [
            ("Only the Information Security Department", False),
            ("Only the heads of business units", False),
            ("Every employee of the Organization", True),
            ("Only the Information Technology Department", False),
        ],
    },
    {
        "chapter": "policy",
        "text": "Where should you report if you have identified or suspect an information security incident?",
        "type": "single",
        "choices": [
            ("Post in the company's general work chat", False),
            ("To the Information Security Department", True),
            ("Do nothing, handle it yourself", False),
            ("Report it only to a coworker", False),
        ],
    },
    {
        "chapter": "policy",
        "text": "Will an employee be retaliated against for reporting an InfoSec incident in good faith, if the violation is not confirmed?",
        "type": "single",
        "choices": [
            ("Yes, false alarms are subject to disciplinary action", False),
            ("No, the Organization guarantees no retaliation regardless of whether the violation is confirmed", True),
            ("This is decided by the direct manager", False),
            ("It depends on who exactly violated the requirements", False),
        ],
    },
    # --- passwords ---
    {
        "chapter": "passwords",
        "text": "What is the minimum password length set for a standard user account?",
        "type": "single",
        "choices": [("6 characters", False), ("8 characters", True), ("10 characters", False), ("14 characters", False)],
    },
    {
        "chapter": "passwords",
        "text": "What is the minimum password length set for a privileged account?",
        "type": "single",
        "choices": [("8 characters", False), ("10 characters", False), ("12 characters", True), ("16 characters", False)],
    },
    {
        "chapter": "passwords",
        "text": "What should you do if a password is compromised or suspected of being compromised?",
        "type": "single",
        "choices": [
            ("Nothing, as long as the password still works", False),
            ("Immediately change the password and notify the IT and InfoSec Departments", True),
            ("Report it a month later at a scheduled meeting", False),
            ("Keep using the password without telling anyone", False),
        ],
    },
    {
        "chapter": "passwords",
        "text": "Is it allowed to save a work resource password in the browser (the \"remember me\" checkbox)?",
        "type": "single",
        "choices": [
            ("Yes, it's convenient and safe", False),
            ("No, you should decline the browser's offer to save the password", True),
            ("Yes, if the password is complex enough", False),
            ("Only allowed for external (non-work) sites", False),
        ],
    },
    {
        "chapter": "passwords",
        "text": "Select all actions a user is PROHIBITED from doing with a password.",
        "type": "multiple",
        "choices": [
            ("Sharing the password with other employees, including their manager", True),
            ("Storing logins and passwords in an unencrypted text file", True),
            ("Using the same password for work and personal (external) resources", True),
            ("Memorizing the password without writing it down anywhere", False),
        ],
    },
    # --- workstation ---
    {
        "chapter": "workstation",
        "text": "What must you do when leaving your workstation?",
        "type": "single",
        "choices": [
            ("Leave the computer as is, do nothing", False),
            ("Lock the workstation", True),
            ("Just turn off the monitor", False),
            ("Only close the currently open window", False),
        ],
    },
    {
        "chapter": "workstation",
        "text": "Which key combination quickly locks a Windows workstation?",
        "type": "single",
        "choices": [("Ctrl + Alt + Del", False), ("Win + L", True), ("Alt + F4", False), ("Ctrl + L", False)],
    },
    {
        "chapter": "workstation",
        "text": "Is a user allowed to independently change settings or disable antivirus protection?",
        "type": "single",
        "choices": [
            ("Yes, if it's getting in the way of work", False),
            ("No, this is prohibited", True),
            ("Yes, with a coworker's verbal agreement", False),
            ("Yes, but only temporarily", False),
        ],
    },
    {
        "chapter": "workstation",
        "text": "What should you do before using a USB drive on a work computer?",
        "type": "single",
        "choices": [
            ("Open the files on it right away", False),
            ("Scan it with antivirus tools", True),
            ("Format the drive", False),
            ("Nothing, external media is always safe", False),
        ],
    },
    # --- internet ---
    {
        "chapter": "internet",
        "text": "How can you make sure a website you're visiting is genuine?",
        "type": "single",
        "choices": [
            ("Just look at the company logo", False),
            ("Carefully verify the exact site address and the presence of a valid certificate (https)", True),
            ("A site is always genuine if it's at the top of search results", False),
            ("There's no need to check", False),
        ],
    },
    {
        "chapter": "internet",
        "text": "Your browser shows a warning: \"This site's security certificate is not trusted.\" What should you do?",
        "type": "single",
        "choices": [
            ("Click \"Continue anyway\" and proceed", False),
            ("Close the site and do not proceed - it could be fake", True),
            ("Ignore it, it's a common technical glitch", False),
            ("Restart the computer and try again", False),
        ],
    },
    {
        "chapter": "internet",
        "text": "What's the right way to react to pop-ups promising a big prize or gift from a contest you never entered?",
        "type": "single",
        "choices": [
            ("Click it to check whether it's real", False),
            ("Decline - it's a sign of a fraudulent site", True),
            ("Enter your work details there", False),
            ("Forward the link to coworkers", False),
        ],
    },
    {
        "chapter": "internet",
        "text": "Is it allowed to run files downloaded from the internet without scanning them first?",
        "type": "single",
        "choices": [
            ("Yes, if the site looks trustworthy", False),
            ("No, files must always be scanned by antivirus before running", True),
            ("Yes, it's always safe", False),
            ("Only allowed for files with a .exe extension", False),
        ],
    },
    # --- email ---
    {
        "chapter": "email",
        "text": "What should you check first when you receive an email with an unexpected request or link?",
        "type": "single",
        "choices": [
            ("Only the body of the email", False),
            ("The exact sender address and where the link actually leads (by hovering over it)", True),
            ("The formatting and signature of the email", False),
            ("The time the email was received", False),
        ],
    },
    {
        "chapter": "email",
        "text": "What should you do with an attachment in an email from an unknown sender?",
        "type": "single",
        "choices": [
            ("Open it if the subject line seems important", False),
            ("Don't open the attachment and report it to the InfoSec Department", True),
            ("Forward the attachment to coworkers so they can check it", False),
            ("Open it in a separate browser window", False),
        ],
    },
    {
        "chapter": "email",
        "text": "What's the correct way to handle 'chain letters' ('good luck' emails, etc.) forwarded to you?",
        "type": "single",
        "choices": [
            ("Forward it further along the chain", False),
            ("Don't take part in forwarding such emails", True),
            ("Reply to everyone in the chain", False),
            ("Save the email in a separate folder for later", False),
        ],
    },
    {
        "chapter": "email",
        "text": "Is it allowed to forward the Organization's confidential information to a personal email (mail.ru, gmail.com, etc.)?",
        "type": "single",
        "choices": [
            ("Yes, if you need to work from home", False),
            ("No, this is prohibited", True),
            ("Yes, with a coworker's verbal consent", False),
            ("Allowed no more than once a month", False),
        ],
    },
    {
        "chapter": "email",
        "text": "The company uses the domain \"example.com\". An email arrives from \"support@exarnple.com\". How should you assess this?",
        "type": "single",
        "choices": [
            ("Nothing unusual, the address looks correct", False),
            ("This is a lookalike domain spoof - a clear sign of phishing", True),
            ("This is a shortened version of the official domain", False),
            ("This is how VIP senders are marked", False),
        ],
    },
]
