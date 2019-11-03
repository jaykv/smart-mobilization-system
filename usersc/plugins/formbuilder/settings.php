<?php
require_once '../../../users/init.php';
$db = DB::getInstance();
if(!in_array($user->data()->id,$master_account)){ Redirect::to($us_url_root.'users/admin.php');} //only allow master accounts to manage plugins! ?>
<?php
include "plugin_info.php";
pluginActive($plugin_name);
require_once $abs_us_root.$us_url_root.'usersc/plugins/formbuilder/assets/fb_displayform.php';
?>
<!DOCTYPE html>
<html>
    <head>
        <title>Form Builder Settings</title>
        <?php require_once $abs_us_root.$us_url_root.'usersc/plugins/formbuilder/assets/bootstrap4.php'; ?>
        <script type="text/JavaScript" src="assist/formbuilder.js"></script>
    </head>
    <body>
        <?php require_once $abs_us_root.$us_url_root.'usersc/plugins/formbuilder/assets/fb_nav_bar.php';?>
        <div id="page-wrapper">
            <div class="container">
                <div class="row justify-content-md-center">
                    <?php
                    $options = ['navigation'=>$us_url_root."usersc/plugins/formbuilder/index.php"];
                    fb_displayform('fb_settings',$options);
                    ?>
                </div>
            </div>
        </div>
    </body>
</html>

