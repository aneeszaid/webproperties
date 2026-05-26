pipeline {
    agent any

    environment {
        OUTPUT_DIR = "/home/ubuntu/excel"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git 'https://github.com/aneeszaid/webproperties.git'
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                /usr/bin/python3 -m venv myenv
                '''
            }
        }

        stage('Run Script') {
            steps {
                sh '''
                source myenv/bin/activate

                # ✅ Create unique filename with timestamp
                TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
                OUTPUT_FILE="redirect_results_$TIMESTAMP.xlsx"

                # ✅ Run script
                python redirect_check.py

                # ✅ Move output file
                mkdir -p $OUTPUT_DIR
                mv redirect_results.xlsx $OUTPUT_DIR/$OUTPUT_FILE
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Job completed successfully"
        }
        failure {
            echo "❌ Job failed"
        }
    }
}
