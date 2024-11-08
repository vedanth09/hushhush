function onFormSubmit(e) {
  var formResponses = e.values;
  var candidateName = formResponses[2];
  var candidateEmail = formResponses[1];
  var candidateAvailabityDate = formResponses[5];
  var candidateAvailabityTime = formResponses[6];
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var dateTime = new Date(candidateAvailabityDate + " " + candidateAvailabityTime);
  var timeDifference = dateTime - new Date();
  var uniqueColabLink = createUniqueColabLink(candidateName);
  var lastRow = sheet.getLastRow();
  sheet.getRange(lastRow, 8).setValue(uniqueColabLink);

  if (timeDifference > 0) {
    ScriptApp.newTrigger('sendEmailNotification').timeBased().after(timeDifference).create();
    PropertiesService.getUserProperties().setProperty('notificationEmail', candidateEmail);
    PropertiesService.getUserProperties().setProperty('candidateName', candidateName);
    PropertiesService.getUserProperties().setProperty('colabLink', uniqueColabLink);
  }
}

function sendEmailNotification() {
  var candidateName = PropertiesService.getUserProperties().getProperty('candidateName');
  var email = PropertiesService.getUserProperties().getProperty('notificationEmail');
  var colabLink = PropertiesService.getUserProperties().getProperty('colabLink');
  var body = "Hi " + candidateName + ",\n\n" + 
             "Thank you for filling out the form. You have been selected for the next phase of the recruitment process.\n\n" +
             "Please complete the coding challenge using your unique Google Colab link:\n" + colabLink + "\n\n" +
             "Good luck!\n\nBest regards,\nDoodle Recruitment Team";

  if (email) {
    MailApp.sendEmail(email, "Doodle Recruitment Coding Challenge", body);
    PropertiesService.getUserProperties().deleteProperty('notificationEmail');
    PropertiesService.getUserProperties().deleteProperty('candidateName');
    PropertiesService.getUserProperties().deleteProperty('colabLink');
  }
}

function createUniqueColabLink(candidateName) {
  var originalColabLink = 'https://colab.research.google.com/drive/1voDbkeYImbWyqwXelr_ya8nh4Yf0qXgu?usp=sharing';
  var fileId = originalColabLink.includes('/drive/') ? originalColabLink.split('/drive/')[1].split('?')[0] : null;
  if (!fileId) return null;
  var copy = DriveApp.getFileById(fileId).makeCopy("Colab_" + candidateName + "_Recruitment_Challenge");
  copy.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.EDIT);
  return "https://colab.research.google.com/drive/" + copy.getId();
}

function checkForEvaluation() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  for (var row = 2; row <= sheet.getLastRow(); row++) {
    var evaluationStatus = sheet.getRange(row, 9).getValue();
    var emailSentStatus = sheet.getRange(row, 10).getValue();
    var candidateEmail = sheet.getRange(row, 2).getValue();
    var candidateName = sheet.getRange(row, 3).getValue();
    var feedback = sheet.getRange(row, 11).getValue();

    if ((evaluationStatus === "Selected" || evaluationStatus === "Not Selected") && emailSentStatus !== "Yes") {
      sendEvaluationEmail(candidateEmail, candidateName, evaluationStatus, feedback);
      sheet.getRange(row, 10).setValue("Yes");
    }
  }
}

function sendEvaluationEmail(email, candidateName, evaluationStatus, feedback) {
  var body = "Hi " + candidateName + ",\n\n" +
             "Thank you for submitting your coding challenge. We have evaluated your submission.\n\n" +
             "Your result: " + evaluationStatus + "\n\n";

  if (evaluationStatus === "Selected") {
    body += "Congratulations! We look forward to proceeding with the next steps.";
  } else if (evaluationStatus === "Not Selected") {
    body += "We regret to inform you that you have not been selected for this role at this time.\n\n";
    body += feedback && feedback.trim() !== "" ? "Feedback/Comments: " + feedback + "\n\n" : "No specific feedback was provided.\n\n";
  }

  body += "\nBest regards,\nDoodle Recruitment Team";
  MailApp.sendEmail(email, "Doodle Recruitment Results", body);
}
