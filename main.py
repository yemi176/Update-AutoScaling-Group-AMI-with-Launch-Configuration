import sys
import boto3
import datetime
from logger import logging

time_stamp = str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# define client
asg_client = boto3.client('autoscaling')

#  Tạo 1 AMI từ 1 instance bất kỳ thuộc ASG đã cho ở trên.


def CreateNewAmiFromInstance(asg_name):
    try:
        asg_info = asg_client.describe_auto_scaling_groups(
            AutoScalingGroupNames=[
                asg_name
            ]
        )
        # Instance config
        instanceID = asg_info['AutoScalingGroups'][0]['Instances'][0]['InstanceId']
        instance_client = boto3.client('ec2')
        # AMI config
        latest_ami = instance_client.create_image(
            Description="AMI for " + asg_name + " created at the" +
            str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S")),
            DryRun=False,
            InstanceId=instanceID,
            Name="AMI-" + str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S")))

        ami_id = latest_ami['ImageId']
        return ami_id
    except Exception as e:
        print(e)
    return False

# - Lấy LC hiện tại của ASG và update lại sử dụng AMI mới.


def CreateNewLC(asg_name, ami_id):
    try:
        asg_info = asg_client.describe_auto_scaling_groups(
            AutoScalingGroupNames=[
                asg_name
            ]
        )

    # LC config
        LcOldName = asg_info['AutoScalingGroups'][0]['LaunchConfigurationName']
        # print(LcOldName)
        LcOldInfo = asg_client.describe_launch_configurations(
            LaunchConfigurationNames=[
                LcOldName,
            ])
        # - Giữ nguyên tất cả cấu hình cũ (key, sg, instancetype, iamrole, userdata).
        sourceInstanceId = asg_info.get('AutoScalingGroups')[
            0]['Instances'][0]['InstanceId']
        keypair = LcOldInfo['LaunchConfigurations'][0]['KeyName']
        sg = LcOldInfo['LaunchConfigurations'][0]['SecurityGroups']
        instance_type = LcOldInfo['LaunchConfigurations'][0]['InstanceType']
        # iamrole = LcOldInfo['LaunchConfigurations'][0]['IamInstanceProfile']
        userdata = LcOldInfo['LaunchConfigurations'][0]['UserData']

    # clone to newLC + # - Đặt tên LC mới có prefix là thời gian tạo.
        lastest_lc = asg_client.create_launch_configuration(
            InstanceId=sourceInstanceId,
            LaunchConfigurationName=str(
                datetime.datetime.now().strftime("%Y%m%d-%H%M%S")) + "-LC",
            ImageId=ami_id,
            KeyName=keypair,
            SecurityGroups=sg,
            UserData=userdata,
            InstanceType=instance_type
        )

        lc_name = lastest_lc['LaunchConfigurationName']
        return lc_name
    except Exception as e:
        print(e)
    return False


# - Update lại ASG sử dụng LC vừa tạo.
def UpdateAsgWithNewLC(asg_name, ):
    lastest_ami = CreateNewAmiFromInstance(asg_name)
    lastest_lc_name = CreateNewLC(asg_name, lastest_ami)
    try:
        response = asg_client.update_auto_scaling_group(
            AutoScalingGroupName=asg_name, LaunchConfigurationName=lastest_lc_name)

        return 'Updated ASG `%s` with new launch configuration `%s` which includes AMI `%s`.' % (asg_name, lastest_lc_name, lastest_ami)
    except Exception as e:
        print(e)
    return False


if __name__ == "__main__":
    asg_name = sys.argv[0]
    UpdateAsgWithNewLC(asg_name)
