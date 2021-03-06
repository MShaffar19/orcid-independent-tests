node {

    properties([
        buildDiscarder(
            logRotator(artifactDaysToKeepStr: '5', artifactNumToKeepStr: '5', daysToKeepStr: '', numToKeepStr: '5')
        ),
        parameters([
            string(name: 'branch_to_build'       , defaultValue: 'master'                               , description: 'Branch name to work on'),
            string(name: 'test_server'           , defaultValue: 'qa.orcid.org'                         , description: 'Base domain name to test'),
            string(name: 'user_login'            , defaultValue: 'jan4@mailinator.com'                  , description: 'Username'),
            string(name: 'user_pass'             , defaultValue: 'test1234'                             , description: 'Password'),
            string(name: 'user_orcid_id'         , defaultValue: '0000-0002-5243-3233'                  , description: 'Latest orcid ID'),
            string(name: 'user_api_id'           , defaultValue: 'APP-CY6IU882C8WLCEVB'                 , description: 'Client ID'),
            string(name: 'user_api_pass'         , defaultValue: '756f9530-ab5f-4e2f-8a27-5b6d5e4b649b' , description: 'Client SECRET')
        ]),
        [$class: 'RebuildSettings', autoRebuild: false, rebuildDisabled: false]
    ])

    git url: 'https://github.com/ORCID/orcid-independent-tests.git', branch: params.branch_to_build

    stage('configure'){
        sh "rm -f orcid/properties.py"
        writeFile file: 'testinputs.py', text: "test_server=\"$test_server\"\nuser_orcid_id=\"$user_orcid_id\"\nuser_login=\"$user_login\"\nuser_pass=\"$user_pass\"\nuser_api_id=\"$user_api_id\"\nuser_api_pass=\"$user_api_pass\"\n"
        sh "cat /var/lib/jenkins/orcidclients.py testinputs.py > orcid/properties.py"
        sh "rm -rf .py_env results"
        sh "virtualenv .py_env"
        sh "mkdir results ${WORKSPACE}/xvfb_jenkins_py"
        sh ". .py_env/bin/activate && pip2 install -r orcid/requirements.txt"
    }

    stage('Test OpenId'){
        try {
            startBrowser()
            pytest 'test_oauth_open_id'
        } catch(Exception err) {
            def err_msg = err.getMessage()
            echo "Tests problem: $err_msg"
        } finally {
            stopBrowser()
            junit 'results/*.xml'
            deleteDir()
            throw err
        }
    }
}
def pytest(unit){
    try{
        sh "export DISPLAY=:1.0 ; . .py_env/bin/activate && py.test --junitxml results/${unit}.xml orcid/${unit}.py"
    } catch(Exception err) {
        throw err
    }
}
def startBrowser(){
    echo "Creating xvfb..."
    sh "Xvfb :1 -screen 0 1024x758x16 -fbdir ${WORKSPACE}/xvfb_jenkins_py & > /dev/null 2>&1 && echo \$! > /tmp/xvfb_jenkins_py.pid"
    sh "cat /tmp/xvfb_jenkins_py.pid"
}
def stopBrowser(){
    echo "Destroying xvfb..."
    sh "XVFB_PID=\$(cat /tmp/xvfb_jenkins_py.pid) ; kill \$XVFB_PID" 
}
