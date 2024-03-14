import xml.etree.ElementTree as ET


def initialize(x):
    x['DistributeSplitEventsConstraint'] = []
    x['SpreadEventsConstraint'] = []
    x['AvoidUnavailableTimes'] = []


def parseResource(resource):
    resource_id = resource.get('Id')
    resource_data = {}
    resource_data['AvoidUnavailableTimes'] = []
    resource_data['ClusterBusyTimes'] = []
    resource_data['Id'] = resource_id
    # Check if Name element exists
    name_element = resource.find('Name')
    if name_element is not None:
        resource_data['Name'] = name_element.text
    else:
        resource_data['Name'] = None

    resource_type = resource.find('.//ResourceType')
    if resource_type is not None:
        resource_data['ResourceType'] = resource_type.get('Reference')
    else:
        resource_data['ResourceType'] = None

    # Check if TimeGroup element exists
    resource_data['ResourceGroups'] = []
    for resource_group in resource.findall('.//ResourceGroup'):
        resource_data['ResourceGroups'].append(resource_group.get('Reference'))
        resourceGroups[resource_group.get('Reference')].append(resource.get('Id'))
    return resource_data


# Parse the XML file
tree = ET.parse('data.xml')
root = tree.getroot()

# Define dictionaries to store parsed data
instances = {}
times = {}
resources = {}
events = {}
timeGroups = {}
resourceGroups = {}
resourceGroupsConstraints = {}
eventGroups = {}
distribute_split_events = {}
spread_events = {}
avoid_unavailable_times = {}
limit_idle_times = {}
cluster_busy_times = {}
prefer_times = {}

# Parse instances
for instance in root.findall('.//Instance'):
    instance_id = instance.get('Id')
    instance_data = {}
    for meta_data in instance.findall('.//MetaData'):
        instance_data['Name'] = meta_data.find('Name').text
        instance_data['Contributor'] = meta_data.find('Contributor').text
        instance_data['Date'] = meta_data.find('Date').text
        instance_data['Country'] = meta_data.find('Country').text
        instance_data['Description'] = meta_data.find('Description').text
        instance_data['Remarks'] = meta_data.find('Remarks').text
    instances[instance_id] = instance_data

# Parse time groups
for time_group in root.findall('.//Times/TimeGroups/TimeGroup'):
    ref = time_group.get('Id')
    timeGroups[ref] = []
for time_group in root.findall('.//Times/TimeGroups/Day'):
    ref = time_group.get('Id')
    timeGroups[ref] = []

# Parse times
for time in root.findall('.//Time'):
    time_id = time.get('Id')
    time_data = {}

    # Check if Name element exists
    name_element = time.find('Name')
    if name_element is not None:
        time_data['Name'] = name_element.text
    else:
        time_data['Name'] = None

    day_element = time.find('Day')
    if day_element is not None:
        time_data['Day'] = day_element.get('Reference')
        timeGroups[time_data['Day']].append(time_id)
    else:
        time_data['Day'] = None

    # Check if TimeGroup element exists
    time_data['TimeGroup'] = []
    for time_group_element in time.findall('.//TimeGroups/TimeGroup'):
        if time_group_element is not None:
            time_data['TimeGroup'].append(time_group_element.get('Reference'))
            timeGroups[time_group_element.get('Reference')].append(time_id)

    times[time_id] = time_data

# Parse resource groups
for res_group in root.findall('.//ResourceGroups/ResourceGroup'):
    ref = res_group.get('Id')
    resourceGroups[ref] = []
    data = {}
    data['LimitIdleTimes'] = []
    resourceGroupsConstraints[ref] = data

# Parse resources
for resource in root.findall('.//Resource'):
    resource_data = parseResource(resource)
    resources[resource_data['Id']] = resource_data

# Parse event groups
for ev_group in root.findall('.//Events/EventGroups/EventGroup'):
    ref = ev_group.get('Id')
    eventGroups[ref] = []

for ev_group in root.findall('.//Events/EventGroups/Course'):
    ref = ev_group.get('Id')
    eventGroups[ref] = []

# Parse events
for event in root.findall('.//Event'):
    event_id = event.get('Id')
    event_data = {}
    event_data['Id'] = event_id
    initialize(event_data)
    # Check if Name element exists
    event_name = event.find('Name')
    if event_name is not None:
        event_data['Name'] = event_name.text
    else:
        event_data['Name'] = None

    duration_element = event.find('Duration')
    if duration_element is not None:
        dur = duration_element.text
        if dur is not None:
            event_data['Duration'] = int(dur)
        else:
            event_data['Duration'] = None
    else:
        event_data['Duration'] = None

    # Check if TimeGroup element exists
    event_data['EventGroups'] = []
    for event_group_element in event.findall('.//EventGroups/EventGroup'):
        event_data['EventGroups'].append(event_group_element.get('Reference'))
        eventGroups[event_group_element.get('Reference')].append(event_id)
    for event_group_element in event.findall('.//Course'):
        event_data['EventGroups'].append(event_group_element.get('Reference'))
        eventGroups[event_group_element.get('Reference')].append(event_id)
    event_data['Resources'] = []
    ress = event.find('Resources')
    if ress is not None:
        for res in ress.findall('.//Resource'):
            res_data = {}
            if res is not None:
                res_ref = res.get('Reference')
            else:
                res_ref = None
            # print(res_ref is None)
            event_data['Resources'].append(res_ref)
    if event_group_element is not None:
        event_data['EventGroup'] = event_group_element.get('Reference')
    else:
        event_data['EventGroup'] = None
    events[event_id] = event_data

# PreferTimesConstraint
for c in root.findall('.//PreferTimesConstraint'):
    c_data = {}
    id = c.get('Id')
    el = c.find('CostFunction')
    if el is not None:
        c_data['CostFunction'] = el.text
    el = c.find('Required')
    if el is not None:
        c_data['Required'] = el.text
    el = c.find('Duration')
    if el is not None:
        c_data['Duration'] = el.text
    el = c.find('Minimum')
    if el is not None:
        c_data['Minimum'] = el.text
    el = c.find('Maximum')
    if el is not None:
        c_data['Maximum'] = el.text
    el = c.find('Weight')
    if el is not None:
        c_data['Weight'] = el.text
    c_data['EventGroups'] = []
    c_data['TimeGroups'] = []
    for e in c.findall('.//AppliesTo/EventGroups/EventGroup'):
        c_data['EventGroups'].append(e.get('Reference')[3:])
    for e in c.findall('.//TimeGroups/TimeGroup'):
        c_data['TimeGroups'].append(e.get('Reference')[3:])
        # print(ref)
    prefer_times[id] = c_data

for c in root.findall('.//DistributeSplitEventsConstraint'):
    c_data = {}
    id = c.get('Id')
    el = c.find('CostFunction')
    if el is not None:
        c_data['CostFunction'] = el.text
    el = c.find('Required')
    if el is not None:
        c_data['Required'] = el.text
    el = c.find('Duration')
    if el is not None:
        c_data['Duration'] = el.text
    el = c.find('Minimum')
    if el is not None:
        c_data['Minimum'] = el.text
    el = c.find('Maximum')
    if el is not None:
        c_data['Maximum'] = el.text
    el = c.find('Weight')
    if el is not None:
        c_data['Weight'] = el.text
    for e in c.findall('.//AppliesTo/EventGroups/EventGroup'):
        ref = e.get('Reference')[3:]
        events[ref]['DistributeSplitEventsConstraint'].append(id)
        # print(ref)
    distribute_split_events[id] = c_data

for c in root.findall('.//SpreadEventsConstraint'):
    c_data = {}
    id = c.get('Id')
    el = c.find('CostFunction')
    if el is not None:
        c_data['CostFunction'] = el.text
    el = c.find('Required')
    if el is not None:
        c_data['Required'] = el.text
    el = c.find('Duration')
    if el is not None:
        c_data['Duration'] = el.text
    el = c.find('Weight')
    if el is not None:
        c_data['Weight'] = el.text
    c_data['EventGroups'] = []
    for e in c.findall('.//EventGroups/EventGroup'):
        ref = e.get('Reference')[3:]
        c_data['EventGroups'].append(e.get('Reference'))
        events[ref]['SpreadEventsConstraint'].append(id)

    c_data['Times'] = []
    for t in c.findall('.//TimeGroups/TimeGroup'):
        ref = t.get('Reference')
        new_data = {}
        new_data['TimeGroup'] = ref
        el = t.find('Minimum')
        if el is not None:
            new_data['Minimum'] = el.text
        el = t.find('Maximum')
        if el is not None:
            new_data['Maximum'] = el.text
        c_data['Times'].append(new_data)

    spread_events[id] = c_data

for c in root.findall('.//LimitIdleTimesConstraint'):
    c_data = {}
    id = c.get('Id')
    el = c.find('CostFunction')
    if el is not None:
        c_data['CostFunction'] = el.text
    el = c.find('Required')
    if el is not None:
        c_data['Required'] = el.text
    el = c.find('Duration')
    if el is not None:
        c_data['Duration'] = el.text
    el = c.find('Weight')
    if el is not None:
        c_data['Weight'] = el.text

    for r in c.findall('.//AppliesTo/ResourceGroups/ResourceGroup'):
        ref = r.get('Reference')
        resourceGroupsConstraints[ref]['LimitIdleTimes'].append(id)

    c_data['TimeGroups'] = []
    for t in c.findall('.//TimeGroups/TimeGroup'):
        ref = t.get('Reference')
        c_data['TimeGroups'].append(ref)

    limit_idle_times[id] = c_data

for c in root.findall('.//AvoidUnavailableTimesConstraint'):
    c_data = {}
    id = c.get('Id')
    el = c.find('CostFunction')
    if el is not None:
        c_data['CostFunction'] = el.text
    el = c.find('Required')
    if el is not None:
        c_data['Required'] = el.text
    el = c.find('Duration')
    if el is not None:
        c_data['Duration'] = el.text
    el = c.find('Weight')
    if el is not None:
        c_data['Weight'] = el.text

    for r in c.findall('.//AppliesTo/Resources/Resource'):
        ref = r.get('Reference')
        resources[ref]['AvoidUnavailableTimes'].append(id)

    c_data['Times'] = []
    for t in c.findall('.//Times/Time'):
        ref = t.get('Reference')
        c_data['Times'].append(ref)

    avoid_unavailable_times[id] = c_data

for c in root.findall('.//ClusterBusyTimesConstraint'):
    c_data = {}
    id = c.get('Id')
    el = c.find('CostFunction')
    if el is not None:
        c_data['CostFunction'] = el.text
    el = c.find('Required')
    if el is not None:
        c_data['Required'] = el.text
    el = c.find('Weight')
    if el is not None:
        c_data['Weight'] = el.text
    el = c.find('Minimum')
    if el is not None:
        c_data['Minimum'] = el.text
    el = c.find('Maximum')
    if el is not None:
        c_data['Maximum'] = el.text

    for r in c.findall('.//AppliesTo/Resources/Resource'):
        ref = r.get('Reference')
        resources[ref]['ClusterBusyTimes'].append(id)

    c_data['TimeGroups'] = []
    for t in c.findall('.//TimeGroups/TimeGroup'):
        ref = t.get('Reference')
        c_data['TimeGroups'].append(ref)

    cluster_busy_times[id] = c_data

print(times)
print(resources)
print(events)
print(distribute_split_events)
print(spread_events)
print(avoid_unavailable_times)
print(limit_idle_times)
print(cluster_busy_times)
print(timeGroups)
print(resourceGroups)
print(eventGroups)
print(resourceGroupsConstraints)
print(prefer_times)
