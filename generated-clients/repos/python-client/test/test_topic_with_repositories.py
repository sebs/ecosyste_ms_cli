# coding: utf-8

"""
    Ecosyste.ms: Repos

    An open API service providing repository metadata for many open source software ecosystems.

    The version of the OpenAPI document: 1.0.0
    Contact: support@ecosyste.ms
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from ecosyste_ms_cli.clients.repos.models.topic_with_repositories import TopicWithRepositories

class TestTopicWithRepositories(unittest.TestCase):
    """TopicWithRepositories unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> TopicWithRepositories:
        """Test TopicWithRepositories
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `TopicWithRepositories`
        """
        model = TopicWithRepositories()
        if include_optional:
            return TopicWithRepositories(
                name = '',
                repositories_count = 56,
                topic_url = '',
                related_topics = [
                    ecosyste_ms_cli.clients.repos.models.topic.Topic(
                        name = '', 
                        repositories_count = 56, 
                        topic_url = '', )
                    ],
                repositories = [
                    ecosyste_ms_cli.clients.repos.models.repository.Repository(
                        id = 56, 
                        uuid = '', 
                        full_name = '', 
                        owner = '', 
                        description = '', 
                        archived = True, 
                        fork = True, 
                        pushed_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        size = 56, 
                        stargazers_count = 56, 
                        open_issues_count = 56, 
                        forks_count = 56, 
                        subscribers_count = 56, 
                        default_branch = '', 
                        last_synced_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        etag = '', 
                        topics = [
                            ''
                            ], 
                        latest_commit_sha = '', 
                        homepage = '', 
                        language = '', 
                        has_issues = True, 
                        has_wiki = True, 
                        has_pages = True, 
                        mirror_url = '', 
                        source_name = '', 
                        license = '', 
                        status = '', 
                        scm = '', 
                        pull_requests_enabled = True, 
                        icon_url = '', 
                        metadata = ecosyste_ms_cli.clients.repos.models.metadata.metadata(), 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        dependencies_parsed_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        dependency_job_id = '', 
                        html_url = '', 
                        previous_names = [
                            ''
                            ], 
                        tags_count = 56, 
                        template = True, 
                        template_full_name = '', 
                        latest_tag_name = '', 
                        latest_tag_published_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        repository_url = '', 
                        tags_url = '', 
                        releases_url = '', 
                        manifests_url = '', 
                        owner_url = '', 
                        download_url = '', 
                        commit_stats = ecosyste_ms_cli.clients.repos.models.commit_stats.commit_stats(), 
                        host = ecosyste_ms_cli.clients.repos.models.host.Host(
                            name = '', 
                            url = '', 
                            kind = '', 
                            repositories_count = 56, 
                            owners_count = 56, 
                            icon_url = '', 
                            host_url = '', 
                            repositoris_url = '', 
                            repository_names_url = '', 
                            owners_url = '', 
                            version = '', 
                            created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), ), )
                    ]
            )
        else:
            return TopicWithRepositories(
        )
        """

    def testTopicWithRepositories(self):
        """Test TopicWithRepositories"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
