<?php

    require_once __DIR__ . "/includes/api.class.php";
    require_once __DIR__ . "/includes/geckoboard.class.php";

    $api = new myApi();
    $gecko = new myGeckoboard();

    $incidents = $api->unresolvedIncidents();
    if(count($incidents) > 0) {
        $msg = "";
        foreach($incidents as $incident) {
            $msg .= "<span style='background-color: red;'>{$incident['platform_name']} - {$incident['product_name']} is <strong>DOWN!</strong></span>\n\n";
        }
    } else {
        $msg = "<center style='background-color: green;'><strong>OK</strong></center>";
    }

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