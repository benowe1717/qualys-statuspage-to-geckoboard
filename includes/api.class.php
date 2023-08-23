<?php

    class myApi {

        private $file = __DIR__ . "/.creds.ini";
        private $apikey = "";
        private $pageid = "";
        private $proxy = "";

        public $scheme = "https://";
        public $domain = "";
        public $version = "";
        public $url = "";
        public $proxy_status = FALSE;

        public $ignored_statuses = array("under_maintenance", "operational");
        public $platforms = array();

        function __construct() {
            if(!is_file($this->file)) {
                echo "ERROR: Unable to read credentials file!\n";
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
                echo "ERROR: Unable to get API credentials!\n";
                exit(1);
            }

            if(isset($arr["proxy"])) {
                if($arr["proxy"]["status"] == 1) {
                    $this->proxy_status = TRUE;
                    $this->proxy = $arr["proxy"]["address"];
                }
            } else {
                echo "ERROR: Unable to determine proxy status!\n";
                exit(1);
            }

            $this->url = "{$this->scheme}{$this->domain}/{$this->version}";
            $result = $this->getPlatforms();
            if($result === FALSE) {
                echo "ERROR: Unable to enumerate Platforms!\n";
                exit(1);
            }
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
            if($this->proxy_status) {
                curl_setopt($ch, CURLOPT_PROXY, $this->proxy);
            }
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

        private function getPlatforms() {
            /*
             * Call the Component Groups API endpoint, which for us is our
             * Platform Names. Grab the ID and Name and store the in the 
             * public array so we can reference them later if needed
             * https://developer.statuspage.io/#operation/getPagesPageIdComponentGroups
            */
            $i = 1;
            $endpoint = "component-groups";
            $response = $this->callApi($endpoint, $i);
            if($response !== FALSE && $response["status"] === 200) {
                $platforms = $response["msg"];
                foreach($platforms as $platform) {
                    $id = $platform["id"];
                    $name = $platform["name"];
                    $this->platforms[$id] = $name;
                }
            } else {
                return FALSE;
            }
        }

        public function unresolvedIncidents() {
            /*
             * Call the Unresolved Incidents API endpoint, which should only
             * list OPEN incidents of any kind. Specifically though, we are 
             * checking if this is an OUTAGE, not for maintenance. If an 
             * OUTAGE is found, add it to the array for returning later, else
             * do nothing.
             * https://developer.statuspage.io/#operation/getPagesPageIdIncidentsUnresolved
            */
            $arr = array();
            $i = 1;
            $endpoint = "incidents/unresolved";
            $response = $this->callApi($endpoint, $i);
            while($response !== FALSE && $response["status"] === 200) {
                if(count($response["msg"]) > 0) {
                    foreach($response["msg"] as $incidents) {
                        foreach($incidents["components"] as $component) {
                            if(!in_array($component["status"], $this->ignored_statuses)) {
                                $id = $component["id"];
                                $product_name = $component["name"];
                                $platform_name = $this->platforms[$component["group_id"]];
                                $arr[$id] = array("platform_name" => $platform_name, "product_name" => $product_name);
                            }
                        }
                    }
                    $i++;
                    $response = $this->callApi($endpoint, $i);
                } else {
                    break;
                }
            }
            return $arr;
        }

    }

?>