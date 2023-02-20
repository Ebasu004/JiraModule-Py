from jira.client import JIRA
import json


class Ticket:
    def __init__(self, project: str, summary: str, issue_type: str, description: str = None):
        self.id = None
        self.comments = None
        self.project = project
        self.summary = summary
        self.issue_type = issue_type
        self.description = description


class JiraClient:
    def __init__(self, server: str, api: str, username: str, password: str):
        options = {"server": server}
        self.api = api
        self.jira = JIRA(options=options, basic_auth=(username, password))

    def create_ticket(self, ticket: Ticket):
        fields = {
            "project": {"key": ticket.project},
            "summary": ticket.summary,
            "description": ticket.description,
            "issuetype": {"name": ticket.issue_type},
        }
        new_issue = self.jira.create_issue(fields=fields)
        return new_issue

    def get_ticket(self, ticket_id: str) -> Ticket:
        try:
            issue = self.jira.issue(ticket_id)
            summary = issue.fields.summary
            project = issue.fields.project.key
            issue_type = issue.fields.issuetype.name
            description = issue.fields.description
            ticket = Ticket(project, summary, issue_type, description)
            ticket.id = ticket_id
            ticket.comments = self.jira.comments(ticket_id)
            return ticket
        except Exception as e:
            print(f"Error: {e}")
            return None

    def update_ticket(self, ticket: Ticket):
        fields = {
            "summary": ticket.summary,
            "description": ticket.description,
        }
        self.jira.issue(ticket.id).update(fields=fields)

    def delete_ticket(self, ticket_id: str):
        self.jira.issue(ticket_id).delete()


def main():
    with open("info.json", "r") as json_file_info:
        info = json.load(json_file_info)
    jira = JiraClient(info["server"], info["api"], info["username"], info["password"])
    ticket_id = "LAB-3587"
    ticket = jira.get_ticket(ticket_id)
    if ticket:
        print(f"Project: {ticket.project}\nSummary: {ticket.summary}\nIssue Type: {ticket.issue_type}\nDescription:\n{ticket.description}")
        ticket.description = "new description"
        jira.update_ticket(ticket)


if __name__ == "__main__":
    main()
