package com.campaignmasta.data.local.dao;

import android.database.Cursor;
import android.os.CancellationSignal;
import androidx.annotation.NonNull;
import androidx.room.CoroutinesRoom;
import androidx.room.EntityInsertionAdapter;
import androidx.room.RoomDatabase;
import androidx.room.RoomSQLiteQuery;
import androidx.room.SharedSQLiteStatement;
import androidx.room.util.CursorUtil;
import androidx.room.util.DBUtil;
import androidx.sqlite.db.SupportSQLiteStatement;
import com.campaignmasta.data.local.entity.CommunityGroupEntity;
import java.lang.Class;
import java.lang.Exception;
import java.lang.Integer;
import java.lang.Object;
import java.lang.Override;
import java.lang.String;
import java.lang.SuppressWarnings;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.Callable;
import javax.annotation.processing.Generated;
import kotlin.Unit;
import kotlin.coroutines.Continuation;
import kotlinx.coroutines.flow.Flow;

@Generated("androidx.room.RoomProcessor")
@SuppressWarnings({"unchecked", "deprecation"})
public final class CommunityGroupDao_Impl implements CommunityGroupDao {
  private final RoomDatabase __db;

  private final EntityInsertionAdapter<CommunityGroupEntity> __insertionAdapterOfCommunityGroupEntity;

  private final SharedSQLiteStatement __preparedStmtOfMarkSynced;

  public CommunityGroupDao_Impl(@NonNull final RoomDatabase __db) {
    this.__db = __db;
    this.__insertionAdapterOfCommunityGroupEntity = new EntityInsertionAdapter<CommunityGroupEntity>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "INSERT OR REPLACE INTO `community_groups` (`localId`,`serverId`,`name`,`groupType`,`wardName`,`wardId`,`estimatedVotingMembers`,`alignment`,`notes`,`updatedAt`,`syncStatus`) VALUES (?,?,?,?,?,?,?,?,?,?,?)";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement,
          @NonNull final CommunityGroupEntity entity) {
        statement.bindString(1, entity.getLocalId());
        if (entity.getServerId() == null) {
          statement.bindNull(2);
        } else {
          statement.bindLong(2, entity.getServerId());
        }
        statement.bindString(3, entity.getName());
        statement.bindString(4, entity.getGroupType());
        statement.bindString(5, entity.getWardName());
        if (entity.getWardId() == null) {
          statement.bindNull(6);
        } else {
          statement.bindLong(6, entity.getWardId());
        }
        if (entity.getEstimatedVotingMembers() == null) {
          statement.bindNull(7);
        } else {
          statement.bindLong(7, entity.getEstimatedVotingMembers());
        }
        statement.bindString(8, entity.getAlignment());
        statement.bindString(9, entity.getNotes());
        statement.bindString(10, entity.getUpdatedAt());
        statement.bindString(11, entity.getSyncStatus());
      }
    };
    this.__preparedStmtOfMarkSynced = new SharedSQLiteStatement(__db) {
      @Override
      @NonNull
      public String createQuery() {
        final String _query = "UPDATE community_groups SET serverId = ?, syncStatus = 'SYNCED' WHERE localId = ?";
        return _query;
      }
    };
  }

  @Override
  public Object insertAll(final List<CommunityGroupEntity> entities,
      final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        __db.beginTransaction();
        try {
          __insertionAdapterOfCommunityGroupEntity.insert(entities);
          __db.setTransactionSuccessful();
          return Unit.INSTANCE;
        } finally {
          __db.endTransaction();
        }
      }
    }, $completion);
  }

  @Override
  public Object insert(final CommunityGroupEntity entity,
      final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        __db.beginTransaction();
        try {
          __insertionAdapterOfCommunityGroupEntity.insert(entity);
          __db.setTransactionSuccessful();
          return Unit.INSTANCE;
        } finally {
          __db.endTransaction();
        }
      }
    }, $completion);
  }

  @Override
  public Object markSynced(final String localId, final int serverId,
      final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        final SupportSQLiteStatement _stmt = __preparedStmtOfMarkSynced.acquire();
        int _argIndex = 1;
        _stmt.bindLong(_argIndex, serverId);
        _argIndex = 2;
        _stmt.bindString(_argIndex, localId);
        try {
          __db.beginTransaction();
          try {
            _stmt.executeUpdateDelete();
            __db.setTransactionSuccessful();
            return Unit.INSTANCE;
          } finally {
            __db.endTransaction();
          }
        } finally {
          __preparedStmtOfMarkSynced.release(_stmt);
        }
      }
    }, $completion);
  }

  @Override
  public Flow<List<CommunityGroupEntity>> getAllFlow() {
    final String _sql = "SELECT * FROM community_groups ORDER BY wardName ASC, name ASC";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    return CoroutinesRoom.createFlow(__db, false, new String[] {"community_groups"}, new Callable<List<CommunityGroupEntity>>() {
      @Override
      @NonNull
      public List<CommunityGroupEntity> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfLocalId = CursorUtil.getColumnIndexOrThrow(_cursor, "localId");
          final int _cursorIndexOfServerId = CursorUtil.getColumnIndexOrThrow(_cursor, "serverId");
          final int _cursorIndexOfName = CursorUtil.getColumnIndexOrThrow(_cursor, "name");
          final int _cursorIndexOfGroupType = CursorUtil.getColumnIndexOrThrow(_cursor, "groupType");
          final int _cursorIndexOfWardName = CursorUtil.getColumnIndexOrThrow(_cursor, "wardName");
          final int _cursorIndexOfWardId = CursorUtil.getColumnIndexOrThrow(_cursor, "wardId");
          final int _cursorIndexOfEstimatedVotingMembers = CursorUtil.getColumnIndexOrThrow(_cursor, "estimatedVotingMembers");
          final int _cursorIndexOfAlignment = CursorUtil.getColumnIndexOrThrow(_cursor, "alignment");
          final int _cursorIndexOfNotes = CursorUtil.getColumnIndexOrThrow(_cursor, "notes");
          final int _cursorIndexOfUpdatedAt = CursorUtil.getColumnIndexOrThrow(_cursor, "updatedAt");
          final int _cursorIndexOfSyncStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "syncStatus");
          final List<CommunityGroupEntity> _result = new ArrayList<CommunityGroupEntity>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final CommunityGroupEntity _item;
            final String _tmpLocalId;
            _tmpLocalId = _cursor.getString(_cursorIndexOfLocalId);
            final Integer _tmpServerId;
            if (_cursor.isNull(_cursorIndexOfServerId)) {
              _tmpServerId = null;
            } else {
              _tmpServerId = _cursor.getInt(_cursorIndexOfServerId);
            }
            final String _tmpName;
            _tmpName = _cursor.getString(_cursorIndexOfName);
            final String _tmpGroupType;
            _tmpGroupType = _cursor.getString(_cursorIndexOfGroupType);
            final String _tmpWardName;
            _tmpWardName = _cursor.getString(_cursorIndexOfWardName);
            final Integer _tmpWardId;
            if (_cursor.isNull(_cursorIndexOfWardId)) {
              _tmpWardId = null;
            } else {
              _tmpWardId = _cursor.getInt(_cursorIndexOfWardId);
            }
            final Integer _tmpEstimatedVotingMembers;
            if (_cursor.isNull(_cursorIndexOfEstimatedVotingMembers)) {
              _tmpEstimatedVotingMembers = null;
            } else {
              _tmpEstimatedVotingMembers = _cursor.getInt(_cursorIndexOfEstimatedVotingMembers);
            }
            final String _tmpAlignment;
            _tmpAlignment = _cursor.getString(_cursorIndexOfAlignment);
            final String _tmpNotes;
            _tmpNotes = _cursor.getString(_cursorIndexOfNotes);
            final String _tmpUpdatedAt;
            _tmpUpdatedAt = _cursor.getString(_cursorIndexOfUpdatedAt);
            final String _tmpSyncStatus;
            _tmpSyncStatus = _cursor.getString(_cursorIndexOfSyncStatus);
            _item = new CommunityGroupEntity(_tmpLocalId,_tmpServerId,_tmpName,_tmpGroupType,_tmpWardName,_tmpWardId,_tmpEstimatedVotingMembers,_tmpAlignment,_tmpNotes,_tmpUpdatedAt,_tmpSyncStatus);
            _result.add(_item);
          }
          return _result;
        } finally {
          _cursor.close();
        }
      }

      @Override
      protected void finalize() {
        _statement.release();
      }
    });
  }

  @Override
  public Object getPending(final Continuation<? super List<CommunityGroupEntity>> $completion) {
    final String _sql = "SELECT * FROM community_groups WHERE syncStatus = 'PENDING'";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    final CancellationSignal _cancellationSignal = DBUtil.createCancellationSignal();
    return CoroutinesRoom.execute(__db, false, _cancellationSignal, new Callable<List<CommunityGroupEntity>>() {
      @Override
      @NonNull
      public List<CommunityGroupEntity> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfLocalId = CursorUtil.getColumnIndexOrThrow(_cursor, "localId");
          final int _cursorIndexOfServerId = CursorUtil.getColumnIndexOrThrow(_cursor, "serverId");
          final int _cursorIndexOfName = CursorUtil.getColumnIndexOrThrow(_cursor, "name");
          final int _cursorIndexOfGroupType = CursorUtil.getColumnIndexOrThrow(_cursor, "groupType");
          final int _cursorIndexOfWardName = CursorUtil.getColumnIndexOrThrow(_cursor, "wardName");
          final int _cursorIndexOfWardId = CursorUtil.getColumnIndexOrThrow(_cursor, "wardId");
          final int _cursorIndexOfEstimatedVotingMembers = CursorUtil.getColumnIndexOrThrow(_cursor, "estimatedVotingMembers");
          final int _cursorIndexOfAlignment = CursorUtil.getColumnIndexOrThrow(_cursor, "alignment");
          final int _cursorIndexOfNotes = CursorUtil.getColumnIndexOrThrow(_cursor, "notes");
          final int _cursorIndexOfUpdatedAt = CursorUtil.getColumnIndexOrThrow(_cursor, "updatedAt");
          final int _cursorIndexOfSyncStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "syncStatus");
          final List<CommunityGroupEntity> _result = new ArrayList<CommunityGroupEntity>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final CommunityGroupEntity _item;
            final String _tmpLocalId;
            _tmpLocalId = _cursor.getString(_cursorIndexOfLocalId);
            final Integer _tmpServerId;
            if (_cursor.isNull(_cursorIndexOfServerId)) {
              _tmpServerId = null;
            } else {
              _tmpServerId = _cursor.getInt(_cursorIndexOfServerId);
            }
            final String _tmpName;
            _tmpName = _cursor.getString(_cursorIndexOfName);
            final String _tmpGroupType;
            _tmpGroupType = _cursor.getString(_cursorIndexOfGroupType);
            final String _tmpWardName;
            _tmpWardName = _cursor.getString(_cursorIndexOfWardName);
            final Integer _tmpWardId;
            if (_cursor.isNull(_cursorIndexOfWardId)) {
              _tmpWardId = null;
            } else {
              _tmpWardId = _cursor.getInt(_cursorIndexOfWardId);
            }
            final Integer _tmpEstimatedVotingMembers;
            if (_cursor.isNull(_cursorIndexOfEstimatedVotingMembers)) {
              _tmpEstimatedVotingMembers = null;
            } else {
              _tmpEstimatedVotingMembers = _cursor.getInt(_cursorIndexOfEstimatedVotingMembers);
            }
            final String _tmpAlignment;
            _tmpAlignment = _cursor.getString(_cursorIndexOfAlignment);
            final String _tmpNotes;
            _tmpNotes = _cursor.getString(_cursorIndexOfNotes);
            final String _tmpUpdatedAt;
            _tmpUpdatedAt = _cursor.getString(_cursorIndexOfUpdatedAt);
            final String _tmpSyncStatus;
            _tmpSyncStatus = _cursor.getString(_cursorIndexOfSyncStatus);
            _item = new CommunityGroupEntity(_tmpLocalId,_tmpServerId,_tmpName,_tmpGroupType,_tmpWardName,_tmpWardId,_tmpEstimatedVotingMembers,_tmpAlignment,_tmpNotes,_tmpUpdatedAt,_tmpSyncStatus);
            _result.add(_item);
          }
          return _result;
        } finally {
          _cursor.close();
          _statement.release();
        }
      }
    }, $completion);
  }

  @NonNull
  public static List<Class<?>> getRequiredConverters() {
    return Collections.emptyList();
  }
}
