# coding: utf-8

"""
    bmlx api-server.

    Documentation of bmlx api-server apis. To find more info about generating spec from source, please refer to https://goswagger.io/use/spec.html  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


import inspect
import pprint
import re  # noqa: F401
import six

from bmlx_openapi_client.configuration import Configuration


class ExperimentVersion(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'create_time': 'int',
        'cron_workflow_name': 'str',
        'dag': 'list[Node]',
        'db_status': 'int',
        'deployment_running': 'bool',
        'description': 'str',
        'execute_detail': 'str',
        'experiment_id': 'int',
        'id': 'int',
        'name': 'str',
        'namespace': 'str',
        'owner': 'str',
        'package_checksum': 'str',
        'package_uri': 'str',
        'parameters': 'dict(str, str)',
        'pipeline_version_id': 'int',
        'resource_group': 'str',
        'status': 'str',
        'trigger_instantly': 'bool',
        'trigger_type': 'str'
    }

    attribute_map = {
        'create_time': 'create_time',
        'cron_workflow_name': 'cron_workflow_name',
        'dag': 'dag',
        'db_status': 'db_status',
        'deployment_running': 'deployment_running',
        'description': 'description',
        'execute_detail': 'execute_detail',
        'experiment_id': 'experiment_id',
        'id': 'id',
        'name': 'name',
        'namespace': 'namespace',
        'owner': 'owner',
        'package_checksum': 'package_checksum',
        'package_uri': 'package_uri',
        'parameters': 'parameters',
        'pipeline_version_id': 'pipeline_version_id',
        'resource_group': 'resource_group',
        'status': 'status',
        'trigger_instantly': 'trigger_instantly',
        'trigger_type': 'trigger_type'
    }

    def __init__(self, create_time=None, cron_workflow_name=None, dag=None, db_status=None, deployment_running=None, description=None, execute_detail=None, experiment_id=None, id=None, name=None, namespace=None, owner=None, package_checksum=None, package_uri=None, parameters=None, pipeline_version_id=None, resource_group=None, status=None, trigger_instantly=None, trigger_type=None, local_vars_configuration=None):  # noqa: E501
        """ExperimentVersion - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._create_time = None
        self._cron_workflow_name = None
        self._dag = None
        self._db_status = None
        self._deployment_running = None
        self._description = None
        self._execute_detail = None
        self._experiment_id = None
        self._id = None
        self._name = None
        self._namespace = None
        self._owner = None
        self._package_checksum = None
        self._package_uri = None
        self._parameters = None
        self._pipeline_version_id = None
        self._resource_group = None
        self._status = None
        self._trigger_instantly = None
        self._trigger_type = None
        self.discriminator = None

        if create_time is not None:
            self.create_time = create_time
        if cron_workflow_name is not None:
            self.cron_workflow_name = cron_workflow_name
        if dag is not None:
            self.dag = dag
        if db_status is not None:
            self.db_status = db_status
        if deployment_running is not None:
            self.deployment_running = deployment_running
        if description is not None:
            self.description = description
        if execute_detail is not None:
            self.execute_detail = execute_detail
        if experiment_id is not None:
            self.experiment_id = experiment_id
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if namespace is not None:
            self.namespace = namespace
        if owner is not None:
            self.owner = owner
        if package_checksum is not None:
            self.package_checksum = package_checksum
        if package_uri is not None:
            self.package_uri = package_uri
        if parameters is not None:
            self.parameters = parameters
        if pipeline_version_id is not None:
            self.pipeline_version_id = pipeline_version_id
        if resource_group is not None:
            self.resource_group = resource_group
        if status is not None:
            self.status = status
        if trigger_instantly is not None:
            self.trigger_instantly = trigger_instantly
        if trigger_type is not None:
            self.trigger_type = trigger_type

    @property
    def create_time(self):
        """Gets the create_time of this ExperimentVersion.  # noqa: E501


        :return: The create_time of this ExperimentVersion.  # noqa: E501
        :rtype: int
        """
        return self._create_time

    @create_time.setter
    def create_time(self, create_time):
        """Sets the create_time of this ExperimentVersion.


        :param create_time: The create_time of this ExperimentVersion.  # noqa: E501
        :type create_time: int
        """

        self._create_time = create_time

    @property
    def cron_workflow_name(self):
        """Gets the cron_workflow_name of this ExperimentVersion.  # noqa: E501


        :return: The cron_workflow_name of this ExperimentVersion.  # noqa: E501
        :rtype: str
        """
        return self._cron_workflow_name

    @cron_workflow_name.setter
    def cron_workflow_name(self, cron_workflow_name):
        """Sets the cron_workflow_name of this ExperimentVersion.


        :param cron_workflow_name: The cron_workflow_name of this ExperimentVersion.  # noqa: E501
        :type cron_workflow_name: str
        """

        self._cron_workflow_name = cron_workflow_name

    @property
    def dag(self):
        """Gets the dag of this ExperimentVersion.  # noqa: E501


        :return: The dag of this ExperimentVersion.  # noqa: E501
        :rtype: list[Node]
        """
        return self._dag

    @dag.setter
    def dag(self, dag):
        """Sets the dag of this ExperimentVersion.


        :param dag: The dag of this ExperimentVersion.  # noqa: E501
        :type dag: list[Node]
        """

        self._dag = dag

    @property
    def db_status(self):
        """Gets the db_status of this ExperimentVersion.  # noqa: E501


        :return: The db_status of this ExperimentVersion.  # noqa: E501
        :rtype: int
        """
        return self._db_status

    @db_status.setter
    def db_status(self, db_status):
        """Sets the db_status of this ExperimentVersion.


        :param db_status: The db_status of this ExperimentVersion.  # noqa: E501
        :type db_status: int
        """

        self._db_status = db_status

    @property
    def deployment_running(self):
        """Gets the deployment_running of this ExperimentVersion.  # noqa: E501


        :return: The deployment_running of this ExperimentVersion.  # noqa: E501
        :rtype: bool
        """
        return self._deployment_running

    @deployment_running.setter
    def deployment_running(self, deployment_running):
        """Sets the deployment_running of this ExperimentVersion.


        :param deployment_running: The deployment_running of this ExperimentVersion.  # noqa: E501
        :type deployment_running: bool
        """

        self._deployment_running = deployment_running

    @property
    def description(self):
        """Gets the description of this ExperimentVersion.  # noqa: E501


        :return: The description of this ExperimentVersion.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ExperimentVersion.


        :param description: The description of this ExperimentVersion.  # noqa: E501
        :type description: str
        """

        self._description = description

    @property
    def execute_detail(self):
        """Gets the execute_detail of this ExperimentVersion.  # noqa: E501


        :return: The execute_detail of this ExperimentVersion.  # noqa: E501
        :rtype: str
        """
        return self._execute_detail

    @execute_detail.setter
    def execute_detail(self, execute_detail):
        """Sets the execute_detail of this ExperimentVersion.


        :param execute_detail: The execute_detail of this ExperimentVersion.  # noqa: E501
        :type execute_detail: str
        """

        self._execute_detail = execute_detail

    @property
    def experiment_id(self):
        """Gets the experiment_id of this ExperimentVersion.  # noqa: E501


        :return: The experiment_id of this ExperimentVersion.  # noqa: E501
        :rtype: int
        """
        return self._experiment_id

    @experiment_id.setter
    def experiment_id(self, experiment_id):
        """Sets the experiment_id of this ExperimentVersion.


        :param experiment_id: The experiment_id of this ExperimentVersion.  # noqa: E501
        :type experiment_id: int
        """

        self._experiment_id = experiment_id

    @property
    def id(self):
        """Gets the id of this ExperimentVersion.  # noqa: E501


        :return: The id of this ExperimentVersion.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ExperimentVersion.


        :param id: The id of this ExperimentVersion.  # noqa: E501
        :type id: int
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this ExperimentVersion.  # noqa: E501


        :return: The name of this ExperimentVersion.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ExperimentVersion.


        :param name: The name of this ExperimentVersion.  # noqa: E501
        :type name: str
        """

        self._name = name

    @property
    def namespace(self):
        """Gets the namespace of this ExperimentVersion.  # noqa: E501


        :return: The namespace of this ExperimentVersion.  # noqa: E501
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this ExperimentVersion.


        :param namespace: The namespace of this ExperimentVersion.  # noqa: E501
        :type namespace: str
        """

        self._namespace = namespace

    @property
    def owner(self):
        """Gets the owner of this ExperimentVersion.  # noqa: E501


        :return: The owner of this ExperimentVersion.  # noqa: E501
        :rtype: str
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """Sets the owner of this ExperimentVersion.


        :param owner: The owner of this ExperimentVersion.  # noqa: E501
        :type owner: str
        """

        self._owner = owner

    @property
    def package_checksum(self):
        """Gets the package_checksum of this ExperimentVersion.  # noqa: E501


        :return: The package_checksum of this ExperimentVersion.  # noqa: E501
        :rtype: str
        """
        return self._package_checksum

    @package_checksum.setter
    def package_checksum(self, package_checksum):
        """Sets the package_checksum of this ExperimentVersion.


        :param package_checksum: The package_checksum of this ExperimentVersion.  # noqa: E501
        :type package_checksum: str
        """

        self._package_checksum = package_checksum

    @property
    def package_uri(self):
        """Gets the package_uri of this ExperimentVersion.  # noqa: E501

        根据pipeline version 中的默认的package uri 和 创建实验时候的参数，将package 重新打包 并上传至ceph  # noqa: E501

        :return: The package_uri of this ExperimentVersion.  # noqa: E501
        :rtype: str
        """
        return self._package_uri

    @package_uri.setter
    def package_uri(self, package_uri):
        """Sets the package_uri of this ExperimentVersion.

        根据pipeline version 中的默认的package uri 和 创建实验时候的参数，将package 重新打包 并上传至ceph  # noqa: E501

        :param package_uri: The package_uri of this ExperimentVersion.  # noqa: E501
        :type package_uri: str
        """

        self._package_uri = package_uri

    @property
    def parameters(self):
        """Gets the parameters of this ExperimentVersion.  # noqa: E501


        :return: The parameters of this ExperimentVersion.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """Sets the parameters of this ExperimentVersion.


        :param parameters: The parameters of this ExperimentVersion.  # noqa: E501
        :type parameters: dict(str, str)
        """

        self._parameters = parameters

    @property
    def pipeline_version_id(self):
        """Gets the pipeline_version_id of this ExperimentVersion.  # noqa: E501


        :return: The pipeline_version_id of this ExperimentVersion.  # noqa: E501
        :rtype: int
        """
        return self._pipeline_version_id

    @pipeline_version_id.setter
    def pipeline_version_id(self, pipeline_version_id):
        """Sets the pipeline_version_id of this ExperimentVersion.


        :param pipeline_version_id: The pipeline_version_id of this ExperimentVersion.  # noqa: E501
        :type pipeline_version_id: int
        """

        self._pipeline_version_id = pipeline_version_id

    @property
    def resource_group(self):
        """Gets the resource_group of this ExperimentVersion.  # noqa: E501


        :return: The resource_group of this ExperimentVersion.  # noqa: E501
        :rtype: str
        """
        return self._resource_group

    @resource_group.setter
    def resource_group(self, resource_group):
        """Sets the resource_group of this ExperimentVersion.


        :param resource_group: The resource_group of this ExperimentVersion.  # noqa: E501
        :type resource_group: str
        """

        self._resource_group = resource_group

    @property
    def status(self):
        """Gets the status of this ExperimentVersion.  # noqa: E501


        :return: The status of this ExperimentVersion.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ExperimentVersion.


        :param status: The status of this ExperimentVersion.  # noqa: E501
        :type status: str
        """
        allowed_values = ["Deactivated", "Activated", "Archived"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and status not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def trigger_instantly(self):
        """Gets the trigger_instantly of this ExperimentVersion.  # noqa: E501


        :return: The trigger_instantly of this ExperimentVersion.  # noqa: E501
        :rtype: bool
        """
        return self._trigger_instantly

    @trigger_instantly.setter
    def trigger_instantly(self, trigger_instantly):
        """Sets the trigger_instantly of this ExperimentVersion.


        :param trigger_instantly: The trigger_instantly of this ExperimentVersion.  # noqa: E501
        :type trigger_instantly: bool
        """

        self._trigger_instantly = trigger_instantly

    @property
    def trigger_type(self):
        """Gets the trigger_type of this ExperimentVersion.  # noqa: E501


        :return: The trigger_type of this ExperimentVersion.  # noqa: E501
        :rtype: str
        """
        return self._trigger_type

    @trigger_type.setter
    def trigger_type(self, trigger_type):
        """Sets the trigger_type of this ExperimentVersion.


        :param trigger_type: The trigger_type of this ExperimentVersion.  # noqa: E501
        :type trigger_type: str
        """
        allowed_values = ["Manual-Trigger", "Auto-Trigger"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and trigger_type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `trigger_type` ({0}), must be one of {1}"  # noqa: E501
                .format(trigger_type, allowed_values)
            )

        self._trigger_type = trigger_type

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = inspect.getargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                elif len(args) == 2:
                    return x.to_dict(serialize)
                else:
                    raise ValueError("Invalid argument size of to_dict")
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ExperimentVersion):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ExperimentVersion):
            return True

        return self.to_dict() != other.to_dict()
