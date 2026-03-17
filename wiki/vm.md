# Virtual machine

<h2>Table of contents</h2>

- [What is a VM](#what-is-a-vm)
- [Your VM](#your-vm)
- [Your VM name](#your-vm-name)
  - [`<your-vm-name>` placeholder](#your-vm-name-placeholder)
- [Your VM IP address](#your-vm-ip-address)
  - [`<your-vm-ip-address>` placeholder](#your-vm-ip-address-placeholder)
- [Connect to the correct network](#connect-to-the-correct-network)
- [Go to the VMs site](#go-to-the-vms-site)
- [Create a VM](#create-a-vm)
  - [Create a subscription](#create-a-subscription)
  - [Create a VM using the subscription](#create-a-vm-using-the-subscription)
- [Go to the VM page](#go-to-the-vm-page)
- [Get the IP address of the VM](#get-the-ip-address-of-the-vm)
- [Delete the VM](#delete-the-vm)
- [Troubleshooting](#troubleshooting)
  - [VM takes too long to start](#vm-takes-too-long-to-start)

## What is a VM

A VM (virtual machine) is a software-emulated computer that runs on a physical [host machine](./computer-networks.md#host), with its own [operating system](./operating-system.md#what-is-an-operating-system) and isolated environment.

In this lab, you use a VM provided by the university to deploy and run the application remotely over [`SSH`](./ssh.md#what-is-ssh).

Docs:

- [What is a virtual machine?](https://azure.microsoft.com/en-us/resources/cloud-computing-dictionary/what-is-a-virtual-machine)

## Your VM

The university provides you a virtual machine (VM) for labs and home experiments for the duration of the `Software Engineering Toolkit` course.

You probably won't have access to the VMs after the course finishes.

See [VM image](./vm-info.md) for the information about your VM.

## Your VM name

The name you chose when [creating the VM](#create-a-vm-using-the-subscription).

### `<your-vm-name>` placeholder

[Your VM name](#your-vm-name) (without `<` and `>`).

## Your VM IP address

The [IP address](./computer-networks.md#ip-address) of [your VM](#your-vm) in the `UniversityStudent` [network](./computer-networks.md#what-is-a-network).

See [Get the IP address of your VM](#get-the-ip-address-of-the-vm).

### `<your-vm-ip-address>` placeholder

[Your VM IP address](#your-vm-ip-address) (without `<` and `>`).

Example: `192.0.2.1`.

See [Get the IP address of the VM](#get-the-ip-address-of-the-vm).

## Connect to the correct network

1. Disable `VPN`.

2. Connect your local machine (laptop) to the `Wi-Fi` network `UniversityStudent`.

## Go to the VMs site

1. [Connect to the correct network](#connect-to-the-correct-network).
2. Open the [https://vm.innopolis.university](https://vm.innopolis.university) site in a browser.

## Create a VM

Complete these steps:

<!-- no toc -->
1. [Connect to the correct network](#connect-to-the-correct-network).
2. [Create a subscription](#create-a-subscription).
3. [Create a VM using the subscription](#create-a-vm-using-the-subscription).

### Create a subscription

1. [Connect to the correct network](#connect-to-the-correct-network).
2. [Go to the VMs site](#go-to-the-vms-site).
3. Click `+ NEW`.
4. Click `MY ACCOUNT`.
5. Click `ADD SUBSCRIPTION`.
6. Click `Software Engineering Toolkit`.
7. Click the checkmark.
8. Go to the [`SUBSCRIPTIONS`](https://vm.innopolis.university/#Workspaces/MyAccountExtension/subscriptions) tab.
9. Look at the `SUBSCRIPTION` column.

   You should see there `Software Engineering Toolkit`.

   The `Status` of this subscription can be `Syncing` or `Active`.

   It can be `Syncing` for a long time.

   Nevertheless, you'll be able to [create a VM using this subscription](#create-a-vm-using-the-subscription) in approximately 15 minutes.

   Don't just sit and wait. Complete other steps.

### Create a VM using the subscription

1. [Connect to the correct network](#connect-to-the-correct-network).
2. [Set up `SSH` (LOCA'L)](./vm-access.md#set-up-ssh-local) if it's not yet set up.
3. [Go to the VMs site](#go-to-the-vms-site).
4. Click `+ NEW`.
5. Click `STANDALONE VIRTUAL MACHINE`.
6. Click `FROM GALLERY`.
7. Click `ALL`.
8. Click `Linux Ubuntu 24.04 Software Engineering Toolkit`.
9. Click `->` to go to the page 2.
10. Fill in the fields:
    - `NAME`: Write the name of your VM (we'll refer to it as [`<your-vm-name>`](#your-vm-name-placeholder) in the instructions).
    - `NEW PASSWORD`: Write the password.
    - `CONFIRM`: Write the same password.
    - `ADMINISTRATOR SSH KEY`:
       1. [Get the public `SSH` key (LOCAL)](./vm-access.md#get-the-public-ssh-key-local).
       2. Copy the **full content** of the public key file.
       3. Paste the content into the input field.
11. Note that the user's name on the VM is [`root`](./linux.md#the-user-root).
12. Click `->` to go to the page 3.
13. Go to `NETWORK ADAPTER 1`.
14. Click `Not Connected`.
15. In the drop-down list, click `StudentsCourses01;10.93.24.0/22`.
16. Click checkmark to complete the setup.
17. The VM will become available in approximately 20 minutes.

## Go to the VM page

1. [Connect to the correct network](#connect-to-the-correct-network).
2. [Go to the VMs site](#go-to-the-vms-site).
3. Click `VIRTUALS MACHINES`.
4. Look at the `NAME` column.
5. Click `<your-vm-name>`.
6. Click `DASHBOARD`.
7. You should be on the VM page.

## Get the IP address of the VM

1. [Go to the VM page](#go-to-the-vm-page).
2. Go to the `quick glance` sidebar (on the right).
3. Go to `IP ADDRESS(ES)`.
4. You should see there:

   ```
   StudentsCourses01 - <your-vm-ip-address>
   ```

   See [`<your-vm-ip-address>`](#your-vm-ip-address-placeholder).

   Example: `StudentsCourses01` - `192.0.2.1`

## Delete the VM

1. [Go to the VM page](#go-to-the-vm-page).
2. Click `DELETE`.

## Troubleshooting

Cases:

- [VM takes too long to start](#vm-takes-too-long-to-start)

### VM takes too long to start

1. [Go to the VM page](./vm.md#go-to-the-vm-page).

2. Go to the `quick glance` sidebar.

3. You should see:

   ```terminal
   Status
   Running
   ```

4. Otherwise:

   Option 1: Wait for the status to change.

   Option 2: If the status doesn't change for more than 20 minutes:

     1. To stop the VM, click `STOP`.

     2. To delete the VM, click `DELETE`.
