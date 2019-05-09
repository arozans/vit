from formatter import Marker

class Markers(Marker):
    def format(self, _, task):
        text_markup = []
        width = 0
        if self.mark_tags:
            width, text_markup = self.format_tags(width, text_markup, task['tags'])
        if self.mark_project:
            width, text_markup = self.format_project(width, text_markup, task['project'])
        if self.mark_due and task['due']:
            width, text_markup = self.format_due(width, text_markup, task['due'], task)
        if self.mark_status:
            width, text_markup = self.format_status(width, text_markup, task['status'])
        if self.mark_depends and task['depends']:
            width, text_markup = self.format_blocked(width, text_markup, task['depends'])
        if self.mark_start and task['start']:
            width, text_markup = self.format_active(width, text_markup, task['start'], task)
        for uda_name, uda_type in self.udas.items():
            if getattr(self, 'mark_%s' % uda_name):
                width, text_markup = self.format_uda(width, text_markup, uda_name, uda_type, task[uda_name])
        if task['uuid'] in self.blocking_tasks:
            width, text_markup = self.format_blocking(width, text_markup)
        return (width, '' if width == 0 else text_markup)

    def color_required(self, color):
        return self.require_color and not color

    def add_label(self, color, label, width, text_markup):
        if self.color_required(color) or not label:
            return width, text_markup
        width += len(label)
        text_markup += [(color, label)]
        return width, text_markup

    def format_tags(self, width, text_markup, tags):
        if not tags:
            color = self.colorizer.tag_none()
            label = self.labels['tag.none.label']
            return self.add_label(color, label, width, text_markup)
        elif len(tags) == 1:
            tag = list(tags)[0]
            color = self.colorizer.tag(tag)
            custom_label = 'tag.%s.label' % tag
            label = self.labels['tag.label'] if not custom_label in self.labels else self.labels[custom_label]
            return self.add_label(color, label, width, text_markup)
        else:
            color = self.colorizer.tag('')
            label = self.labels['tag.label']
            return self.add_label(color, label, width, text_markup)

    def format_project(self, width, text_markup, project):
        if not project:
            color = self.colorizer.project_none()
            label = self.labels['project.none.label']
            return self.add_label(color, label, width, text_markup)
        else:
            color = self.colorizer.project(project)
            custom_label = 'project.%s.label' % project
            label = self.labels['project.label'] if not custom_label in self.labels else self.labels[custom_label]
            return self.add_label(color, label, width, text_markup)

    def format_due(self, width, text_markup, due, task):
        due_state = self.defaults.get_due_state(due, task)
        if due_state:
            color = self.colorizer.due(due_state)
            label = self.labels['%s.label' % due_state]
            return self.add_label(color, label, width, text_markup)
        return width, text_markup

    def format_uda(self, width, text_markup, uda_name, uda_type, value):
        if not value:
            color = self.colorizer.uda_none(uda_name)
            label = self.labels['uda.%s.none.label' % uda_name]
            return self.add_label(color, label, width, text_markup)
        else:
            color = getattr(self.colorizer, 'uda_%s' % uda_type)(uda_name, value)
            custom_label = 'uda.%s.label' % uda_name
            label = self.labels['uda.label'] if not custom_label in self.labels else self.labels[custom_label]
            return self.add_label(color, label, width, text_markup)

    def format_blocking(self, width, text_markup):
        color = self.colorizer.blocking()
        label = self.labels['blocking.label']
        return self.add_label(color, label, width, text_markup)

    def format_status(self, width, text_markup, status):
        if status == 'completed' or status == 'deleted':
            color = self.colorizer.status(status)
            label = self.labels['%s.label' % status]
            return self.add_label(color, label, width, text_markup)
        return width, text_markup

    def format_blocked(self, width, text_markup, depends):
        color = self.colorizer.blocked(depends)
        label = self.labels['blocked.label']
        return self.add_label(color, label, width, text_markup)

    def format_active(self, width, text_markup, start, task):
        active = self.defaults.get_active_state(start, task)
        if active:
            color = self.colorizer.active(active)
            label = self.labels['active.label']
            return self.add_label(color, label, width, text_markup)
        return width, text_markup
