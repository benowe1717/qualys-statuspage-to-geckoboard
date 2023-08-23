<?php

    class myApi {

        private $file = __DIR__ . "/.creds.ini";
        private $apikey = "";
        private $pageid = "";

        public $scheme = "https://";
        public $domain = "";
        public $version = "";
        public $url = "";

        function __construct() {
            if(!is_file($this->file)) {
                echo "ERROR: Unable to read credentials file!";
                exit(1);
            } else {
                $arr = parse_ini_file($this->file, TRUE);
            }

            if(isset($arr["api"])) {
                $this->apikey = $arr["api"]["apikey"];
                $this->domain = $arr["api"]["domain"];
                $this->version = $arr["api"]["version"];
                $this->pageid = $arr["api"]["pageid"];
            } else {
                echo "ERROR: Unable to get API credentials!";
                exit(1);
            }

            $this->url = "{$this->scheme}{$this->domain}/{$this->version}";
        }

        private function callApi(string $endpoint, int $page = 0) {
            /*
             * Call the API endpoint using the class' configured
             * Domain, Version, and Page ID along with the given
             * OAuth API Key and return the result
            */
            $url = "{$this->url}/pages/{$this->pageid}/{$endpoint}?page={$page}";
            $headers = [
                "Authorization: OAuth {$this->apikey}"
            ];

            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, $url);
            curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
            $response = curl_exec($ch);
            $status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
            curl_close($ch);

            switch($status_code) {
                case 200:
                    return $arr = array("status" => $status_code, "msg" => json_decode($response, TRUE));
                    break;
                case 401:
                    return $arr = array("status" => $status_code, "msg" => "Could not authenticate");
                    break;
                case 404:
                    return $arr = array("status" => $status_code, "msg" => "The requested resource could not be found.");
                    break;
                default:
                    return FALSE;
                    break;
            }
        }

        public function unresolvedIncidents() {
            $arr = array();
            $i = 1;
            $endpoint = "incidents/unresolved";
            $response = $this->callApi($endpoint, $i);
            while($response !== FALSE && $response["status"] === 200) {
                if(count($response["msg"]) > 0) {
                    print_r($response["msg"]);
                    $i++;
                    $response = $this->callApi($endpoint, $i);
                } else {
                    break;
                }
            }
        }

    }

?>