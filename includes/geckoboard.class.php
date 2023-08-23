<?php

    class myGeckoboard {

        private $file = __DIR__ . "/.creds.ini";
        private $apikey = "";
        private $widget_key = "";
        private $proxy = "";

        public $scheme = "https://";
        public $domain = "";
        public $version = "";
        public $url = "";
        public $proxy_status = FALSE;
        public $status_codes = array(400 => "Response body is empty or invalid JSON", 401 => "You are not authorized to push to this widget",
        403 => "Widget does not support push/Your API key is invalid", 404 => "The widget does not exist", 413 => "The request body is too large",
        429 => "You have exceeded your rate limit");

        function __construct() {
            if(!is_file($this->file)) {
                echo "ERROR: Unable to read credentials file!";
                exit(1);
            } else {
                $arr = parse_ini_file($this->file, TRUE);
            }

            if(isset($arr["gecko"])) {
                $this->apikey = $arr["gecko"]["apikey"];
                $this->domain = $arr["gecko"]["domain"];
                $this->version = $arr["gecko"]["version"];
                $this->widget_key = $arr["gecko"]["widgetkey"];
            } else {
                echo "ERROR: Unable to get Geckoboard credentials!\n";
                exit(1);
            }

            if(isset($arr["proxy"])) {
                if($arr["proxy"]["status"] === 1) {
                    $this->proxy_status = TRUE;
                    $this->proxy = $arr["proxy"]["address"];
                }
            } else {
                echo "ERROR: Unable to determine proxy status!\n";
                exit(1);
            }

            $this->url = "{$this->scheme}{$this->domain}/{$this->version}";
        }

        public function pushToGeckoboard(string $text) {
            /*
             * Call the custom Widget Key API endpoint and post the corresponding
             * text to the widget. All formatting and control of the text can be
             * found in the main.php script.
             * https://developer-custom.geckoboard.com/#details
             * https://developer-custom.geckoboard.com/#text
             * https://support.geckoboard.com/en/articles/6055637-use-the-text-widget-to-display-text-on-your-dashboard#adding_html
            */
            $url = "{$this->url}/send/{$this->widget_key}";
            $payload["api_key"] = $this->apikey;
            $payload["data"]["item"][0]["text"] = $text;
            $payload["data"]["item"][0]["type"] = 1;

            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, $url);
            curl_setopt($ch, CURLOPT_POST, TRUE);
            curl_setopt($ch, CURLOPT_HTTPHEADER, array("Content-Type: application/json"));
            curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
            if($this->proxy_status) {
                curl_setopt($ch, CURLOPT_PROXY, $this->proxy);
            }
            $response = curl_exec($ch);
            $status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
            curl_close($ch);

            $msg = json_decode($response, TRUE);
            if(isset($this->status_codes[$status_code])) {
                return $arr = array("status" => $status_code, "msg" => "{$this->status_codes[$status_code]} :: {$msg['message']}");
            } else {
                return $arr = array("status" => $status_code, "msg" => $msg);
            }
        }

    }

?>