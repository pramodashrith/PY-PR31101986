resource    "aws_instance" "webserver" {
    ami= "ami-0c23fasdfaf"
    instance_type = "t2.micro"
}