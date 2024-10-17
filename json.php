<?php
    $json_file = 'output.json'; // Arquivo JSON gerado pelo Python

    $json_data = json_decode(file_get_contents($json_file), true);
    $processed_data = array();
    $previous_item = array();

    for ($i = 0; $i < count($json_data); $i++) {
        if (empty($json_data[$i]["ID Nome"])) {
            foreach ($json_data[$i] as $json_data_key => $json_data_value) {
                if (!empty($json_data_value)) {
                    if (!empty($previous_item[$json_data_key])) {
                        if (strpos($previous_item[$json_data_key], $json_data_value) === false) {
                            $previous_item[$json_data_key] .= " " . $json_data_value;
                        }
                    } else {
                        $previous_item[$json_data_key] = $json_data_value;
                    }
                }
            }
            $processed_data[count($processed_data) - 1] = $previous_item;
        } else {
            $previous_item = $json_data[$i];
            $processed_data[] = $previous_item;
        }
    }

    echo "<pre> processed data";
    var_dump($processed_data);
    echo "</pre>";
?>