from jira.client import JIRA
import json


class Ticket:

    def __init__(self, project: dict, summary: str, issue_type: dict, description: str = None):
        """Constructor for the Jira ticket object.

        project: Dictionary containing what board to post ticket on.
                 Example:
                     {"key" : "LAB"}
        summary: String containing the title of the of the ticket.
        issue_type: Dictionary containing the issue type.
                    Example:
                        {"name" : "Bug"}
        description (Optional): String containing the description of the ticket.
        """
        self.id = None
        self.comments = None
        self.project = project
        self.summary = summary
        self.issue_type = issue_type
        self.description = description


class Jira:

    def __init__(self):
        with open('info.json', 'r') as json_file_info:
            self.info = json.load(json_file_info)

        self.options = {
            "server": f"{self.info['server']}"
        }

        self.api = f"{self.info['api']}"
        self.user = f"{self.info['username']}"
        self.jira = JIRA(options=self.options, basic_auth=(self.user, self.api))

    def create(self):
        info_dict = {
            'project': {'key': 'LAB'},
            'summary': 'Summary',
            'description': '*Please perform the following tasks*',
            'issuetype': {'name': 'Task'},
        }

        new_issue = self.jira.create_issue(fields=info_dict)
        print(new_issue)

    def get(self, ticket_id):
        """Get ticket from Jira and return a Ticket object.
        ticket_id: String containing the ID of the ticket to retrieve.

        return: Ticket object or None if invalid id is provided."""
        comments = self.jira.comments(ticket_id)
        issue = self.jira.issue(ticket_id)
        print(issue.fields)
        summary = issue.raw["fields"]["summary"]
        project = issue.raw["fields"]["project"]["key"]
        issue_type = issue.raw['fields']['issuetype']['name']
        description = issue.fields.description

        # print(project, '\n', summary, issue_type, description)
        print(f"Project: {project}\nSummary: {summary}\nIssue Type: {issue_type}\nDescription:\n{description}")

        # ticket = Ticket(project, summary, issue_type, description)

    # def get_info(self, ticket_id):
    #     issue = self.jira.issue(ticket_id)
    #     comments = self.jira.comments(ticket_id)
    #     summary = issue.fields.description
    #
    #     print(summary, '\n')
    #
    #     for i in comments:
    #         author = self.jira.comment(ticket_id, i).author.displayName
    #         time = self.jira.comment(ticket_id, i).created
    #         print(author, time, i.body)

    def update_info(self, ticket_id):
        issue = self.jira.issue(ticket_id)
        issue.update(fields={'summary': 'new summary', 'description': 'A new summary was added'})

    def delete(self, ticket_id):
        issue = self.jira.issue(ticket_id)
        issue.delete()


# ticket = Ticket({"key": "LAB"}, "This is a test ticket.", {"name": "Task"})
# jira = Jira
# jira.create(ticket)
# ticket_id = "123"
# ticket = jira.get(ticket_id)
#
# ticket.description = "new description"
# ticket.id = "!23"
# # throws exception if ticket_id is invalid or None
# jira.update(ticket)
j = Jira()
j.get('LAB-3587')
