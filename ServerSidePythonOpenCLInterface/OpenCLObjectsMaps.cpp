/*
Maps to store the dynamic OpenCL objects;
The Objects shall store associations between OpenCL objects and their integer Id. 
The Module uses boost...
*/

#include <CL/cl.h>
#include <map>
#include <stdexcept>

class CLContext{
public:
  typedef cl_context CLType;
  static cl_int Retain(CLType clt){
    return clRetainContext(clt);
  };
  static cl_int Release(CLType clt){
    return clReleaseContext(clt);
  };
};

class CLCommandQueue{
public:
  typedef cl_command_queue CLType;
  static cl_int Retain(CLType clt){
    return clRetainCommandQueue(clt);
  };
  static cl_int Release(CLType clt){
    return clReleaseCommandQueue(clt);
  };
};

class CLMem{
public:
  typedef cl_mem CLType;
  static cl_int Retain(CLType clt){
    return clRetainMemObject(clt);
  };
  static cl_int Release(CLType clt){
    return clReleaseMemObject(clt);
  };
};

class CLProgram{
public:
  typedef cl_program CLType;
  static cl_int Retain(CLType clt){
    return clRetainProgram(clt);
  };
  static cl_int Release(CLType clt){
    return clReleaseProgram(clt);
  };
};

class CLKernel{
public:
  typedef cl_kernel CLType;
  static cl_int Retain(CLType clt){
    return clRetainKernel(clt);
  };
  static cl_int Release(CLType clt){
    return clReleaseKernel(clt);
  };
};

template<class CLObjectWRetainAndRelease>
class CLDataWID{
typedef typename CLObjectWRetainAndRelease::CLType CLType;
private:
  long _ID;
  CLType _pc;
  long _refcount;
public:
  CLDataWID(){
    _ID = 0; 
    _pc = NULL; 
    _refcount = 0;};
  CLDataWID(CLType pc){
    _ID = 0;
    _pc=pc;
    _refcount=1;};
  virtual ~CLDataWID(){};
  inline void SetID(long ID){_ID = ID;};
  inline long GetID(){return _ID;}
  inline long GetRefCount(){return _refcount;};
  inline CLType GetCLObject(){return _pc;};
  inline cl_int Retain(){
    cl_int nErrCode = CLObjectWRetainAndRelease::Retain(_pc);
    if(nErrCode != CL_SUCCESS) return nErrCode;
    _refcount++;
    return CL_SUCCESS;
  };
  inline cl_int Release(long& refCount){
    cl_int nErrCode = CLObjectWRetainAndRelease::Release(_pc);
    if(nErrCode != CL_SUCCESS){
      refCount = _refcount;
      return nErrCode;
    }
    refCount = --_refcount;
    return nErrCode;
  };
};

template<class object_type>
class UniqueIdMap : public std::map<long, object_type>{
public:
  typedef std::map<long, object_type>	BaseClass;
  typedef typename BaseClass::iterator	BaseClassIterator; 
private:
  long  _newId;
  unsigned long _MAX_ELEMENTS;
public:
  UniqueIdMap():_newId(0), _MAX_ELEMENTS(4096){};
  long InsertElement(object_type obj){
    // make sure that there are more slots in the map
    if( this->size() == _MAX_ELEMENTS ) throw std::runtime_error("Out of map resources");
    // find an unused Id
    while( this->find(_newId) != this->end() ) _newId = (_newId + 1) % _MAX_ELEMENTS;
    obj.SetID( _newId++ );
    // insert the object in the map
    (*this)[obj.GetID()] = obj;
    return obj.GetID();
  };
};

typedef  CLDataWID<CLContext> ContextDataWID;
typedef  UniqueIdMap<ContextDataWID> ContextMap;
ContextMap _contextMap;

typedef  CLDataWID<CLCommandQueue> CommandQueueDataWID;
typedef  UniqueIdMap<CommandQueueDataWID> CommandQueueMap;
CommandQueueMap _commandqueueMap;

typedef  CLDataWID<CLMem> MemDataWID;
typedef  UniqueIdMap<MemDataWID> MemMap;
MemMap _memMap;

typedef  CLDataWID<CLProgram> ProgramDataWID;
typedef  UniqueIdMap<ProgramDataWID> ProgramMap;
ProgramMap _programMap;

typedef  CLDataWID<CLKernel> KernelDataWID;
typedef  UniqueIdMap<KernelDataWID> KernelMap;
KernelMap _kernelMap;

extern "C" bool InsertContext(cl_context pc, long *pID){
  try{
    *pID = _contextMap.InsertElement( ContextDataWID(pc) );
    return true;
  }
  catch(std::exception &e){
    *pID = 0;
    return false;
  }
}

extern "C" cl_context GetContext(long id){
  ContextMap::BaseClassIterator it = _contextMap.find(id);
  if(it == _contextMap.end())
    return NULL;
  return it->second.GetCLObject();
}

extern "C" bool RetainContext(long id){
  ContextMap::BaseClassIterator it = _contextMap.find(id);
  if(it == _contextMap.end())
    return false;
  it->second.Retain();
  return true;
}

extern "C" long ReleaseContext(long id){
  ContextMap::BaseClassIterator it = _contextMap.find(id);
  if(it == _contextMap.end())
    return -1;
  long RefCount;
  it->second.Release(RefCount);
  if(RefCount <= 0)
    _contextMap.erase(id);
  return RefCount;
}

extern "C" long GetContextID(cl_context pc){
  ContextMap::BaseClassIterator it;
  for(it = _contextMap.begin(); it != _contextMap.end(); it++)
    if(it->second.GetCLObject() == pc) 
      return it->first;
  return 0l;
}

extern "C" long GetNumberOfContexts(){
  return _contextMap.size();
}

extern "C" void GetContextsIDs(long* ids){
  ContextMap::BaseClassIterator it;
  long ii = 0;
  for(it = _contextMap.begin(); it != _contextMap.end(); it++)
    ids[ii++] = it->first;
}

extern "C" bool InsertCommandQueue(cl_command_queue pc, long *pID){
  try{
    *pID = _commandqueueMap.InsertElement( CommandQueueDataWID(pc) );
    return true;
  }
  catch(std::exception &e){
    *pID = 0;
    return false;
  }
}

extern "C" cl_command_queue GetCommandQueue(long id){
  CommandQueueMap::BaseClassIterator it = _commandqueueMap.find(id);
  if(it == _commandqueueMap.end())
    return NULL;
  return it->second.GetCLObject();
}

extern "C" bool RetainCommandQueue(long id){
  CommandQueueMap::BaseClassIterator it = _commandqueueMap.find(id);
  if(it == _commandqueueMap.end())
    return false;
  it->second.Retain();
  return true;
}

extern "C" long ReleaseCommandQueue(long id){
  CommandQueueMap::BaseClassIterator it = _commandqueueMap.find(id);
  if(it == _commandqueueMap.end())
    return -1;
  long RefCount;
  it->second.Release(RefCount);
  if(RefCount <= 0)
    _commandqueueMap.erase(id);
  return RefCount;
}

extern "C" long GetCommandQueueID(cl_command_queue pc){
  CommandQueueMap::BaseClassIterator it;
  for(it = _commandqueueMap.begin(); it != _commandqueueMap.end(); it++)
    if(it->second.GetCLObject() == pc) 
      return it->first;
  return 0l;
}

extern "C" long GetNumberOfCommandQueues(){
  return _commandqueueMap.size();
}

extern "C" void GetCommandQueuesIDs(long* ids){
  CommandQueueMap::BaseClassIterator it;
  long ii = 0;
  for(it = _commandqueueMap.begin(); it != _commandqueueMap.end(); it++)
    ids[ii++] = it->first;
}

extern "C" bool InsertMem(cl_mem pc, long *pID){
  try{
    *pID = _memMap.InsertElement( MemDataWID(pc) );
    return true;
  }
  catch(std::exception &e){
    *pID = 0;
    return false;
  }
}

extern "C" cl_mem GetMem(long id){
  MemMap::BaseClassIterator it = _memMap.find(id);
  if(it == _memMap.end())
    return NULL;
  return it->second.GetCLObject();
}

extern "C" bool RetainMem(long id){
  MemMap::BaseClassIterator it = _memMap.find(id);
  if(it == _memMap.end())
    return false;
  it->second.Retain();
  return true;
}

extern "C" long ReleaseMem(long id){
  MemMap::BaseClassIterator it = _memMap.find(id);
  if(it == _memMap.end())
    return -1;
  long RefCount;
  it->second.Release(RefCount);
  if(RefCount <= 0)
    _memMap.erase(id);
  return RefCount;
}

extern "C" long GetMemID(cl_mem pc){
  MemMap::BaseClassIterator it;
  for(it = _memMap.begin(); it != _memMap.end(); it++)
    if(it->second.GetCLObject() == pc) 
      return it->first;
  return 0l;
}

extern "C" long GetNumberOfMems(){
  return _memMap.size();
}

extern "C" void GetMemsIDs(long* ids){
  MemMap::BaseClassIterator it;
  long ii = 0;
  for(it = _memMap.begin(); it != _memMap.end(); it++)
    ids[ii++] = it->first;
}

extern "C" bool InsertProgram(cl_program pc, long *pID){
  try{
    *pID = _programMap.InsertElement( ProgramDataWID(pc) );
    return true;
  }
  catch(std::exception &e){
    *pID = 0;
    return false;
  }
}

extern "C" cl_program GetProgram(long id){
  ProgramMap::BaseClassIterator it = _programMap.find(id);
  if(it == _programMap.end())
    return NULL;
  return it->second.GetCLObject();
}

extern "C" bool RetainProgram(long id){
  ProgramMap::BaseClassIterator it = _programMap.find(id);
  if(it == _programMap.end())
    return false;
  it->second.Retain();
  return true;
}

extern "C" long ReleaseProgram(long id){
  ProgramMap::BaseClassIterator it = _programMap.find(id);
  if(it == _programMap.end())
    return -1;
  long RefCount;
  it->second.Release(RefCount);
  if(RefCount <= 0)
    _programMap.erase(id);
  return RefCount;
}

extern "C" long GetProgramID(cl_program pc){
  ProgramMap::BaseClassIterator it;
  for(it = _programMap.begin(); it != _programMap.end(); it++)
    if(it->second.GetCLObject() == pc) 
      return it->first;
  return 0l;
}

extern "C" long GetNumberOfPrograms(){
  return _programMap.size();
}

extern "C" void GetProgramsIDs(long* ids){
  ProgramMap::BaseClassIterator it;
  long ii = 0;
  for(it = _programMap.begin(); it != _programMap.end(); it++)
    ids[ii++] = it->first;
}

extern "C" bool InsertKernel(cl_kernel pc, long *pID){
  try{
    *pID = _kernelMap.InsertElement( KernelDataWID(pc) );
    return true;
  }
  catch(std::exception &e){
    *pID = 0;
    return false;
  }
}

extern "C" cl_kernel GetKernel(long id){
  KernelMap::BaseClassIterator it = _kernelMap.find(id);
  if(it == _kernelMap.end())
    return NULL;
  return it->second.GetCLObject();
}

extern "C" bool RetainKernel(long id){
  KernelMap::BaseClassIterator it = _kernelMap.find(id);
  if(it == _kernelMap.end())
    return false;
  it->second.Retain();
  return true;
}

extern "C" long ReleaseKernel(long id){
  KernelMap::BaseClassIterator it = _kernelMap.find(id);
  if(it == _kernelMap.end())
    return -1;
  long RefCount;
  it->second.Release(RefCount);
  if(RefCount <= 0)
    _kernelMap.erase(id);
  return RefCount;
}

extern "C" long GetKernelID(cl_kernel pc){
  KernelMap::BaseClassIterator it;
  for(it = _kernelMap.begin(); it != _kernelMap.end(); it++)
    if(it->second.GetCLObject() == pc) 
      return it->first;
  return 0l;
}

extern "C" long GetNumberOfKernels(){
  return _kernelMap.size();
}

extern "C" void GetKernelsIDs(long* ids){
  KernelMap::BaseClassIterator it;
  long ii = 0;
  for(it = _kernelMap.begin(); it != _kernelMap.end(); it++)
    ids[ii++] = it->first;
}

// devices and platforms

#define MAX_PLATFORMS 2
#define MAX_DEVICES 10

cl_platform_id _platforms[MAX_PLATFORMS];
unsigned int _NPlatforms = 0;
cl_device_id _devices[MAX_DEVICES];
unsigned int _NDevices = 0;

extern "C" int InitializePlatformAndDevices(int device_type){
  cl_int nErr = clGetPlatformIDs(1, _platforms, &_NPlatforms);
  if(nErr == CL_SUCCESS){
    cl_device_type dev_type = CL_DEVICE_TYPE_GPU;
    dev_type = device_type == 1 ? CL_DEVICE_TYPE_CPU : 
               (device_type == 2 ? CL_DEVICE_TYPE_ALL : CL_DEVICE_TYPE_GPU);
    // query the devices
    nErr = clGetDeviceIDs(_platforms[0], dev_type, MAX_DEVICES, _devices, &_NDevices);
  }
  return nErr;
}

extern "C" long GetNumberOfDevices(void){
  return _NDevices;
}

extern "C" void GetDevicesIds(long id[]){
  for(unsigned int ii = 0; ii < _NDevices; ii++) id[ii] = ii;
}

extern "C" long GetDeviceID(cl_device_id clDevID){
  for(unsigned int ii = 0; ii < _NDevices; ii++)
    if(_devices[ii] == clDevID) return (long)ii;
  return -1;
}

extern "C" cl_device_id GetCLDevice(long id){
  return ((id < _NDevices && id >= 0) ? _devices[id] : NULL);
}

extern "C" cl_platform_id GetCLPlatform(long id){
  if(id < 0 || id > _NPlatforms) return NULL;
  return _platforms[id];
}

