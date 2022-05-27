import axios, { AxiosRequestConfig } from "axios";
import { Group, GroupID, Host, HostID } from "../types/fog";

export async function queryFogGroups() {
  const config: AxiosRequestConfig = {
    headers: {
      "fog-api-token": process.env.FOG_API_TOKEN as string,
      "fog-user-token": process.env.FOG_USER_TOKEN as string,
    },
  };

  // Query groups
  const groupsRequest = await axios.get<{ groups: Group[] }>(
    `${process.env.FOG_URL}/group`,
    config
  );
  const groups = groupsRequest.data.groups;

  type HostDict = { [hostID: HostID]: Host };
  const groupsDict: { [groupID: GroupID]: Group & { hosts: HostDict } } = {};
  for (const group of groups) {
    groupsDict[group.id] = { ...group, hosts: {} };
  }

  // Query hosts
  const hostsRequest = await axios.get<{ hosts: Host[] }>(
    `${process.env.FOG_URL}/host`,
    config
  );
  const hosts = hostsRequest.data.hosts;
  const hostsDict: HostDict = {};
  for (const host of hosts) {
    hostsDict[host.id] = host;
  }

  // Query associations group <-> host
  type GroupAssociations = {
    groupassociations: { id: string; hostID: HostID; groupID: GroupID }[];
  };

  const groupAssociationQuery = await axios.get<GroupAssociations>(
    `${process.env.FOG_URL}/groupassociation`,
    config
  );
  const groupAssociation = groupAssociationQuery.data.groupassociations;

  for (const assoc of groupAssociation) {
    const group = groupsDict[assoc.groupID];

    if (group) {
      group.hosts[assoc.hostID] = hostsDict[assoc.hostID];
    }
  }

  return groupsDict;
}

export async function queryFogHosts() {
  const config: AxiosRequestConfig = {
    headers: {
      "fog-api-token": process.env.FOG_API_TOKEN as string,
      "fog-user-token": process.env.FOG_USER_TOKEN as string,
    },
  };

  type HostDict = { [hostID: HostID]: Host };

  // Query hosts
  const hostsRequest = await axios.get<{ hosts: Host[] }>(
    `${process.env.FOG_URL}/host`,
    config
  );
  const hosts = hostsRequest.data.hosts;
  const hostsDict: HostDict = {};
  
  for (const host of hosts) {
    hostsDict[host.id] = host;
  }
  return hostsDict;
}
