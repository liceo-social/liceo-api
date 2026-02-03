# from typing import Annotated

# from fastapi import Depends

# from liceo.labs.scheduler import Scheduler, SchedulerSingleton
# from liceo.security.registration.adapters.di import RegistrationJobs


# def load_scheduler(registration: RegistrationJobs) -> Scheduler:
#     # CREATE INSTANCE
#     scheduler = SchedulerSingleton.instance()

#     # ADD JOB COLLECTIONS
#     scheduler.add_job_collections([registration])

#     # RETURN DEPENDENCY
#     return scheduler


# SchedulerDependency = Annotated[Scheduler, Depends(load_scheduler)]
