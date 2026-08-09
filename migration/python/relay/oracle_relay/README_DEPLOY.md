# Deploying the Flattrade Relay on your Oracle Cloud VM

This runs on `flattrade-static-ip-node` (public IP `130.210.22.73`), not on
your home PC. It's the only piece of SENTRY that talks to Flattrade directly.

## Step 1 — Open the port on Oracle Cloud

Oracle's VMs block incoming traffic by default. You need to allow port
`8090` (the port `relay_server.py` listens on):

1. In the Oracle Cloud console, go to your instance → click the **VCN** link
   under "Primary VNIC" → click the **Subnet** → click the **Default
   Security List**.
2. **Add Ingress Rule**: Source CIDR `0.0.0.0/0`, IP Protocol `TCP`,
   Destination Port Range `8090`. Save.

(Optional but safer later: restrict the Source CIDR to your home's public IP
specifically, once you know it, instead of `0.0.0.0/0` — but `0.0.0.0/0` is
fine to get started, since the relay itself requires the shared secret for
anything sensitive.)

## Step 2 — SSH into the VM and set it up

From your home PC's terminal (replace the key path with wherever Oracle gave
you the `.pem`/`.key` file when you created the instance):

```bash
ssh -i /path/to/your-key.pem ubuntu@130.210.22.73
```

(If the VM's OS isn't Ubuntu, Oracle's default is usually `opc` or `ubuntu`
as the username — check the instance details page if `ubuntu` doesn't work.)

Once connected, install Python and set up the project:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
mkdir -p ~/sentry-relay
cd ~/sentry-relay
```

## Step 3 — Upload the relay files

From a **second terminal window on your home PC** (not the SSH session),
copy this whole `oracle_relay` folder to the VM:

```bash
scp -i /path/to/your-key.pem -r oracle_relay/* ubuntu@130.210.22.73:~/sentry-relay/
```

## Step 4 — Configure and run it (back in the SSH session)

```bash
cd ~/sentry-relay
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env
```

Fill in `BROKER_API_KEY`, `BROKER_API_SECRET` (your real Flattrade values),
and make up a long random string for `RELAY_SHARED_SECRET` — save with
`Ctrl+O`, Enter, then `Ctrl+X` to exit nano.

Run it:

```bash
python3 relay_server.py
```

You should see it start listening on port 8090. Test it from your home PC's
own browser or terminal:

```bash
curl http://130.210.22.73:8090/health
```

Should return `{"status": "ok", ...}`.

## Step 5 — Keep it running after you close the SSH session

The command above stops the moment you close the terminal. To keep it
running in the background:

```bash
nohup python3 relay_server.py > relay.log 2>&1 &
```

Now you can safely close the SSH session and it keeps running. Check the log
anytime with:

```bash
tail -f ~/sentry-relay/relay.log
```

(A proper `systemd` service that survives VM reboots automatically is a nicer
long-term setup — worth doing once this is confirmed working, not before.)
