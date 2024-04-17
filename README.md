Astronomer Design Review
========================

Astronomer’s Design Reviews are designed to give your team a hands-on way to uplevel your Airflow usage. Regardless of your team size, experience level, or use case, our experts will provide actionable recommendations to improve your workflow orchestration.

This branch contains information for design review hosts and contributors.

## Instructions and prerequisites for all design reviews

All design review sessions have their own branch in this repo (see [Choosing a design review session](#choosing-a-design-review-session) for more info about the different branches). The `README` in each branch contains instructions for hands-on exercises. The file structure is the same as an Astro project, with an additional folder for `exercise-solutions` where relevant.


Design reviews are intended to be given in person, with one Astronomer presenter and at least one other Astronomer helper. Design review content is not designed for participants to complete asynchronously. 

For each workshop, participants will need:

- An Astro account (a [free trial](https://astronomer.io/try-astro) will work, but ensure it has access to the features covered in the workshop before beginning).
- The [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli)
- [Docker](https://www.docker.com/) 4.0 or greater

## Choosing a design review session

There are four standard design review sessions available on different branches in the repository:

- `introduction-to-airflow`: In this session, we’ll cover everything you need to know to get started with Airflow, including core concepts, the basics of writing pipelines, and how to identify use cases well suited to Airflow. We’ll also cover how to easily get started running Airflow on Astro, including creating deployments, deploying code, and navigating the Astro UI. This design review is suitable for beginner Airflow users.
- `dag-writing-best-practices`: In this session, we'll cover best practices for developing DAGs that make the most of what Airflow has to offer. We’ll also include tips for writing DAGs efficiently with Astro features like the Cloud IDE, Github integration, and more. This design review is suitable for intermediate to advanced Airflow users.
- `best-practices-astro-platform-management`: In this session, we’ll cover best practices for platform teams running Airflow on Astro at scale, including topics like cost optimization, how to identify when teams need new Airflow deployments, how to onboard new development teams quickly, and more.  This design review is suitable for intermediate to advanced Airflow users.
- `airflow-for-gen-ai`: In this session, we’ll provide reference architectures for how to leverage Airflow features to operationalize generative AI workflows and how to implement these workflows at scale on Astro. This design review is suitable for intermediate to advanced Airflow users.

## Contributing and questions

If you would like to contribute to or request a design review, or have any questions about the content, please reach out to the DevRel team.
