# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\resource.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from functools import partial, reduce
from ..base import NamedTuple, Proxy, first, index_if, nop
DEFAULT_PRIORITY = 0

class Resource(object):

    def grab(self, client, *a, **k):
        raise NotImplementedError

    def release(self, client):
        raise NotImplementedError

    def get_owner(self):
        raise NotImplementedError
    owner = property(lambda self: self.get_owner())

class CompoundResource(Resource):
    pass

    def __init__(self, first_resource=None, second_resource=None, *a, **k):
        super(CompoundResource, self).__init__(*a, **k)
        self._first_resource = first_resource
        self._second_resource = second_resource

    def grab(self, client, *a, **k):
        if self._first_resource.grab(client, *a, **k):
            if self._second_resource.grab(client, *a, **k):
                pass
            else:
                self._first_resource.release(client)
        return self.owner == client

    def release(self, client):
        if client == self.owner:
            self._second_resource.release(client)
            self._first_resource.release(client)
            return True
        else:
            return False

    def get_owner(self):
        return self._first_resource.owner or self._second_resource.owner

    @property
    def first(self):
        return self._first_resource

    @property
    def second(self):
        return self._second_resource

def compose_resources(*resources):
    return reduce(CompoundResource, resources)

class ExclusiveResource(Resource):
    pass

    def __init__(self, on_received_callback=None, on_lost_callback=None, *a, **k):
        super(ExclusiveResource, self).__init__(*a, **k)
        self._owner = None
        if on_received_callback:
            self.on_received = on_received_callback
        if on_lost_callback:
            self.on_lost = on_lost_callback

    def grab(self, client, *a, **k):
        if self._owner is None:
            self.on_received(client, *a, **k)
            self._owner = client
        return self._owner == client

    def release(self, client):
        if client == self._owner:
            self._owner = None
            self.on_lost(client)
            return True
        else:
            return False

    def get_owner(self):
        return self._owner

    def on_received(self, client, *a, **k):
        raise NotImplementedError('Override or pass callback')

    def on_lost(self, client):
        raise NotImplementedError('Override or pass callback')

class SharedResource(Resource):
    pass

    def __init__(self, on_received_callback=None, on_lost_callback=None, *a, **k):
        super(SharedResource, self).__init__(*a, **k)
        if on_received_callback:
            self.on_received = on_received_callback
        if on_lost_callback:
            self.on_lost = on_lost_callback
        self._clients = set()

    def grab(self, client, *a, **k):
        self.on_received(client, *a, **k)
        self._clients.add(client)
        return True

    def release(self, client):
        if client in self._clients:
            self.on_lost(client)
            self._clients.remove(client)
            for client in self._clients:
                self.on_received(client)
            return True
        else:
            return False

    def get_owner(self):
        return

    def on_received(self, client, *a, **k):
        raise NotImplementedError('Override or pass callback')

    def on_lost(self, client):
        raise NotImplementedError('Override or pass callback')

class StackingResource(Resource):
    pass

    def __init__(self, on_received_callback=None, on_lost_callback=None, *a, **k):
        super(StackingResource, self).__init__(*a, **k)
        self._clients = []
        self._owners = set()
        if on_received_callback:
            self.on_received = on_received_callback
        if on_lost_callback:
            self.on_lost = on_lost_callback

    def grab(self, client, priority=None):
        if priority is None:
            priority = DEFAULT_PRIORITY
        old_owners = self._owners
        self._remove_client(client)
        self._add_client(client, priority)
        new_owners = self._actual_owners()
        if new_owners != old_owners:
            self._owners = new_owners
            self._on_lost_set(set(old_owners) - set(new_owners))
            self._on_received_set(new_owners)
        return True

    def _on_lost_set(self, clients):
        for client in clients:
            self.on_lost(client)

    def _on_received_set(self, clients):
        for client in clients:
            self.on_received(client)

    def release(self, client):
        old_owners = self._owners
        result = self._remove_client(client)
        new_owners = self._actual_owners()
        if new_owners != old_owners:
            self._owners = new_owners
            self._on_lost_set(set(old_owners) - set(new_owners))
            self._on_received_set(new_owners)
        return result

    def release_all(self):
        pass
        for client, _ in list(self._clients):
            self.release(client)

    def _add_client(self, client, priority):
        idx = index_if(lambda client_and_priority: client_and_priority[1] > priority, self._clients)
        self._clients.insert(idx, (client, priority))

    def _remove_client(self, client):
        idx = index_if(lambda client_and_priority: client_and_priority[0] == client, self._clients)
        if idx != len(self._clients):
            del self._clients[idx]
            return True

    def _actual_owners(self):
        return [self._clients[-1][0]] if self._clients else []

    @property
    def max_priority(self):
        return self._clients[-1][1] if self._clients else DEFAULT_PRIORITY

    @property
    def stack_size(self):
        return len(self._clients)

    def get_owner(self):
        for owner in self._owners:
            return owner
            break

    @property
    def clients(self):
        return list(map(first, self._clients))

    @property
    def owners(self):
        return self._owners

    def on_received(self, client):
        raise NotImplementedError('Override or pass callback')

    def on_lost(self, client):
        raise NotImplementedError('Override or pass callback')

    def release_stacked(self):
        clients = self.clients
        owners = self.owners
        for client in clients:
            if client not in owners:
                self.release(client)
            continue

class PrioritizedResource(StackingResource):
    pass

    def _actual_owners(self):
        max_priority = self.max_priority
        return [client for client, priority in self._clients if priority == max_priority]

class ClientWrapper(NamedTuple):
    wrap = partial(nop)
    unwrap = partial(nop)

class ProxyResource(Proxy):
    pass

    def __init__(self, proxied_resource=None, client_wrapper=ClientWrapper(), *a, **k):
        super(ProxyResource, self).__init__(*a, proxied_object=proxied_resource, **k)
        self._client_wrapper = client_wrapper

    def grab(self, client, *a, **k):
        self.__getattr__('grab')(self._client_wrapper.wrap(client), *a, **k)

    def release(self, client, *a, **k):
        self.__getattr__('release')(self._client_wrapper.wrap(client), *a, **k)

    @property
    def owner(self):
        return self._client_wrapper.unwrap(self.__getattr__('owner'))

    @property
    def owners(self):
        return list(map(self._client_wrapper.unwrap, self.__getattr__('owners')))