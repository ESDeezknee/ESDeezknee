<?php
header("Content-Type:application/json");
$servername = "host.docker.internal";
$username = "root";
$password = "root";
$dbname = "icebreakers";
	
// connect the database with the server
$conn = new mysqli($servername,$username,$password,$dbname,3306);
	
	// if error occurs
	if ($conn -> connect_errno)
	{
	echo "Failed to connect to MySQL: " . $conn -> connect_error;
	exit();
	}

	$rand_no = random_int(1,6);
	$sql = "select * from icebreakers where id = {$rand_no};"  ;
	$result = ($conn->query($sql));
	//declare array to store the data of database
	$row = [];

	if (mysqli_num_rows($result)> 0)
	{
		$row = mysqli_fetch_array($result);
        $id = $row["id"];
        $statement = $row["statement"];
        $response_code = 300;
        $response_desc = "Icebreaker has been returned";
        response($id,$statement);
	}else{
        response(NULL,NULL);
    }

function response($id, $statement){
    $response["id"] = $id;
    $response["statement"] = $statement;

    $json_response = json_encode($response);
    echo $json_response;
}

?>

<?php
echo json_encode($row);
exit();
?>


<?php
	mysqli_close($conn);
?>
