# **MedGuardian**

<h4>Personal Medication Assistant</h4>

<p>MedGuardian provides users a web interface to assist with management of prescription medications.</p>
<h3>FEATURES</h3>
<ul>
  <li>Individualized user login and profile</li>
  <li>Maintain a list of active medical providers (prescribers)</li>
  <li>Entry and storage of prescription medication details
    <ul>
      <li>Database includes  more than 40,000 FDA approved prescription medications</li>
    </ul>
  </li>
  <li>Visualization of all active medication</li>
  <li>Visualization of that day's medication
    <ul>
      <li>Allows downloading of printable PDF of day's medications</li>
    </ul>
  </li>
  <li>Assignment and modification of administration times for each medication</li>
  <li>HIPPA-compliant SMS reminders that medication is due
    <ul>
      <li>Alerts based on user-chosen administration times</li>
    </ul>
  </li>
</ul>

<h3>Technologies</h3>

<h4>Backend</h4>
<ul>
  <li>MedGuardian is built on the Django Web Framework</li>
  <li>Two Python Microservices
    <ul>
      <li>Database population with prescription-related data, including parsing and storage of FDA medication data</li>
      <li>Separate notification service that pushes SMS alerts shortly before medications are to be taken</li>
    </ul>
  </li>
  <li>NGINX proxy server</li>
</ul>

