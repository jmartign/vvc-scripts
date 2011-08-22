<?
session_start();
session_register("session");
//if(!isset($session['userid'])){
//echo "<center><font face='Verdana' size='2' color=red>Sorry, Please login and use this page </font></center>";
//exit;
//}
// This is displayed if all the fields are not filled in
$empty_fields_message = "<p>Please go back and complete all the fields in the form.</p>Click <a class=\"two\" href=\"javascript:history.go(-1)\">here</a> to go back";
// Convert to simple variables 
$password1 = $_POST['password1']; 
$password2 = $_POST['password2'];
if (!isset($_POST['password1'])) {
?>
<h2>Change password! <? echo $_SESSION['email_address']; ?></h2>
<form method="post" action="<?php echo $_SERVER['REQUEST_URI']; ?>">
    <p class="style3"><label for="password1"">New password:</label>
    <input type="password" title="Please enter a password" name="password1" size="30"></p>
    <p class="style3"><label for="password2">Re-enter Password:</label>
    <input type="password" title="Please re-enter password" name="password2" size="30"></p>
    <p style="stext-align:left"><label for="submit">&nbsp</label>
    <input type="submit" value="Change" class="submit-button"/></p>
</form>
<?php
}
elseif (empty($password1) || empty($password2))  {
    echo $empty_fields_message;
}
else {
include 'includes/connection.php'; 
$db_password1=md5(mysql_real_escape_string($password1));
//Setting flags for checking
$status = "OK";
$msg="";
if ( strlen($password1) < 3 or strlen($password1) > 10 ){
$msg=$msg."Password must be more than 3 characters in length and maximum 10 characters in length<BR>";
$status= "NOTOK";}     
if (strcmp( $password1,$password2 ) !=0){
$msg=$msg."Both passwords do not match<BR>";
$status= "NOTOK";}     
if($status<>"OK"){ 
echo "<font face='Verdana' size='2' color=red>$msg</font><br><center><input type='button' value='Retry' onClick='history.go(-1)'></center>";
}else{ // if all validations are passed.
if(mysql_query("update users set password='$db_password1' where userid='$session[userid]'")){
echo "<font face='Verdana' size='2' ><center>Thanks <br> Your password changed successfully. Please keep changing your password for better security</font></center>". $password1;
}
}
}
?> 
