import sys
import json
from client import SlabAllocator

alloc = SlabAllocator(obj_size=64, slab_capacity=4)

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "slab_memory_op",
                        "description": "Allocate or free objects from Slab memory cache pool",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "action": {"type": "string", "enum": ["allocate", "free"]},
                                "obj_id": {"type": "string"}
                            },
                            "required": ["action"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "slab_memory_op":
            act = args["action"]
            if act == "allocate":
                obj = alloc.allocate()
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"action": "allocated", "obj_id": obj, "total_slabs": len(alloc.slabs)})}]}}
            elif act == "free":
                ok = alloc.free(args.get("obj_id", ""))
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"action": "freed", "success": ok})}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if line.strip():
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
