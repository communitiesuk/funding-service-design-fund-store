# Data Updates
## Expected Usage
The configuration of data used to load funds, rounds, sections etc lives [here](/config/fund_loader_config).
Once this data has been loaded, if it needs to change, there are 2 options:
1. Truncate all data in the tables and rerun the [import scripts](/README.md#seeding-fund-data)
1. Update the data in the existing rows.

This folder is intended to serve option 2.

## Script format
When data needs to be updated (after it has already been inserted in UAT/production - for changes during development use option 1 and truncate the data then reinsert).

For each change,
1. Update the main [fund loader config](/config/fund_loader_config/) with any new values.
1. Create a new python script in [data_updates](.). This script should read through the fund loader config and make any required updates.

This approach ensures that data is only defined in one place (fund_loader_config) and then stored in the database.

## Running
To run the script, find the container ID for the fund-store and execute

    docker exec -it <fund_store_container_id> python -m scripts.data_updates.<script_name>

To run on cloud foundry, use `cf run-task`

    cf run-task funding-service-design-fund-store-test --command "python -m scripts.data_updates.patch_cyp_name"

Or to run inside the CF container:

    export PYTHONPATH=/home/vcap/app
    cd app
    LD_LIBRARY_PATH=/home/vcap/deps/0/lib:/home/vcap/deps/0/python/lib:$LD_LIBRARY_PATH ~/deps/0/python/bin/python3.10 ./scripts/data_updates/FS-3471-application_guidance.py
