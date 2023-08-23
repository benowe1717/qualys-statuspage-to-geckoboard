<?php

    require_once __DIR__ . "/includes/api.class.php";
    require_once __DIR__ . "/includes/geckoboard.class.php";

    $api = new myApi();
    $gecko = new myGeckoboard();

    $api->unresolvedIncidents();
    
    $msg = "This is a test message, but from PHP this time";
    $result = $gecko->pushToGeckoboard($msg);
    
    if($result["status"] === 200) {
        if(isset($result["msg"]["success"])) {
            echo "Successfully posted to Geckoboard!\n";
            exit(0);
        }
    } else {
        echo "ERROR: Unable to post to Geckoboard! Status Code: {$result['status']} :: Details: {$result['msg']}\n";
        exit(1);
    }

?>