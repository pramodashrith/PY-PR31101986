resource "local_file" "pet"{
	filename="/Users/pramodashrith/teraform/teraform-local-file/pets.txt"
        content= "we love pets!"
        file_permission = 0700
}