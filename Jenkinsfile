node{
    // Parameters
    def IMAGE_REGISTRY = 'loantran176/asg_ami_update_lc'
    def BUILD_NUMBER = env.BUILD_NUMBER

    // CI
    stage('Checkout SourceCode'){
        sh 'git clone https://github.com/yemi176/Update-AutoScaling-Group-AMI-with-Launch-Configuration.git'
    }
    
    stage('DOCKER_IMAGE_BUILD'){
        
        sh "docker build -t ${IMAGE_REGISTRY}:${BUILD_NUMBER} -f ./Dockerfile"
        sh "docker images"
        sh "docker ps -a"
        
    }
}