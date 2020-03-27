from footmark.oos.oosobject import TaggedOOSObject


class Template(TaggedOOSObject):
    def __init__(self, connection=None):
        super(Template, self).__init__(connection)

    def __repr__(self):
        return 'Template:%s' % self.id

    def __getattr__(self, name):
        if name == 'name':
            return self.template_name
        if name == 'id':
            return self.template_id
        if name == 'version':
            return self.template_version

    def __setattr__(self, name, value):
        if name == 'template_name':
            self.name = value
        if name == 'template_id':
            self.id = value
        if name == 'template_version':
            self.version = value
        if name == 'template':
            for k, v in value.items():
                if k == 'template_id':
                    self.id = v
                if k == 'template_name':
                    self.name = v
                if k == 'template_version':
                    self.version = v
        super(TaggedOOSObject, self).__setattr__(name, value)

    def risk(self):
        return self.connection.list_execution_risky_tasks(template_name=self.name)

    def read(self):
        OOS = {}
        for name, value in list(self.__dict__.items()):
            if name in ["connection", "region_id", "region", "request_id"]:
                continue
            if name == 'template':
                for k, v in value.items():
                    OOS[k] = v
                continue
            OOS[name] = value
        return OOS

    def delete(self):
        return self.connection.delete_template(template_name=self.name)

    def update(self, content):
        if content != self.content:
            return self.connection.update_template(template_name=self.name, content=content)
        return None

    def get(self):
        return self.connection.get_template(template_name=self.name)

    def add_tags(self, tags):
        """
        Add tags
        """
        return self.connection.tag_resources(resource_ids=[self.name], tags=tags, resource_type='template')

    def remove_tags(self, tags):
        """
        remove tags
        """
        return self.connection.untag_resources(resource_ids=[self.name], tags=tags, resource_type='template')


class Executions(TaggedOOSObject):
    def __init__(self, connection=None):
        super(Executions, self).__init__(connection)

    def __repr__(self):
        return 'Executions:%s' % self.id

    def __getattr__(self, name):
        if name == 'name':
            return self.template_name
        if name == 'id':
            return self.execution_id

    def __setattr__(self, name, value):
        if name == 'execution':
            for k, v in value.items():
                if k == 'execution_id':
                    self.id = v
                if k == 'template_name':
                    self.name = v
        super(TaggedOOSObject, self).__setattr__(name, value)

    def read(self):
        execution = {}
        for name, value in list(self.__dict__.items()):
            if name in ["connection", "region_id", "region", "request_id"]:
                continue
            if name == 'execution':
                for k, v in value.items():
                    execution[k] = v
                continue
            execution[name] = value
        return execution
