import libvirt
import xml.etree.ElementTree as ET

def connect():
    return libvirt.open('qemu:///system')

def list_vms():
    conn = connect()
    domains = conn.listAllDomains()
    vms = [{"name": d.name(), "state": d.state()[0]} for d in domains]
    conn.close()
    return vms

def start_vm(vm_name):
    conn = connect()
    domain = conn.lookupByName(vm_name)
    if domain.state()[0] == libvirt.VIR_DOMAIN_SHUTOFF:
        domain.create()
        conn.close()
        return True
    conn.close()
    return False

def stop_vm(vm_name):
    conn = connect()
    domain = conn.lookupByName(vm_name)
    if domain.state()[0] == libvirt.VIR_DOMAIN_RUNNING:
        domain.shutdown()
        conn.close()
        return True
    conn.close()
    return False

def create_vm(vm_name, memory, vcpus):
    conn = connect()
    xml_template = f"""
    <domain type='kvm'>
      <name>{vm_name}</name>
      <memory unit='KiB'>{memory * 1024}</memory>
      <vcpu>{vcpus}</vcpu>
      <os>
        <type arch='x86_64' machine='pc-i440fx-6.0'>hvm</type>
      </os>
      <devices>
        <disk type='file' device='disk'>
          <source file='/var/lib/libvirt/images/{vm_name}.img'/>
          <target dev='vda' bus='virtio'/>
        </disk>
        <interface type='network'>
          <source network='default'/>
        </interface>
      </devices>
    </domain>
    """
    try:
        domain = conn.defineXML(xml_template)
        domain.create()
        conn.close()
        return True
    except Exception as e:
        print(f"Error creating VM: {e}")
        conn.close()
        return False
